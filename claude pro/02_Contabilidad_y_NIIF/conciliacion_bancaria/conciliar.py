"""
Conciliacion bancaria automatizada.

    python conciliar.py libros.csv extracto.csv
    python conciliar.py libros.xlsx extracto.xlsx --saldo-inicial 185000000 --dias 3

Como cruza
----------
1. Cruce exacto por referencia / numero de comprobante.
2. A lo que quede sin cruzar le aplica un segundo cruce por VALOR con tolerancia
   de fecha (por defecto +/- 5 dias): asi aparecen las partidas en transito.
3. Lo que sobra se clasifica en:
     - SOLO EN LIBROS   -> cheques girados y no cobrados, consignaciones en transito
     - SOLO EN EXTRACTO -> GMF, comisiones, rendimientos, notas debito y credito
     - DIFERENCIA DE VALOR -> misma referencia, distinto importe (error de digitacion)
4. Prueba aritmetica:
     saldo extracto + partidas solo en libros - partidas solo en extracto = saldo en libros

Columnas de LIBROS   : fecha, referencia (o comprobante), valor (o debito/credito), descripcion
Columnas de EXTRACTO : fecha, referencia, valor, descripcion
Los nombres se normalizan; si no hay 'valor' se calcula como debito - credito.
"""
from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import pandas as pd

ALIAS = {
    "comprobante": "referencia", "documento": "referencia", "num_documento": "referencia",
    "nro_documento": "referencia", "no_documento": "referencia", "doc": "referencia",
    "detalle": "descripcion", "concepto": "descripcion", "observacion": "descripcion",
    "importe": "valor", "monto": "valor", "valor_movimiento": "valor",
    "debe": "debito", "haber": "credito",
}


def normalizar(col: str) -> str:
    s = unicodedata.normalize("NFKD", str(col)).encode("ascii", "ignore").decode()
    s = s.strip().lower().replace(" ", "_")
    return ALIAS.get(s, s)


def cargar(ruta: Path, etiqueta: str) -> pd.DataFrame:
    df = (pd.read_excel(ruta) if ruta.suffix.lower().startswith(".xls")
          else pd.read_csv(ruta, sep=None, engine="python"))
    df.columns = [normalizar(c) for c in df.columns]

    if "valor" not in df.columns:
        if {"debito", "credito"} <= set(df.columns):
            df["valor"] = (pd.to_numeric(df["debito"], errors="coerce").fillna(0)
                           - pd.to_numeric(df["credito"], errors="coerce").fillna(0))
        else:
            raise SystemExit(f"[{etiqueta}] necesita una columna 'valor' o 'debito'/'credito'.")
    df["valor"] = pd.to_numeric(df["valor"], errors="coerce").fillna(0.0).round(2)

    if "referencia" not in df.columns:
        raise SystemExit(f"[{etiqueta}] necesita una columna 'referencia' o 'comprobante'.")
    df["referencia"] = df["referencia"].astype(str).str.strip().str.upper()

    df["fecha"] = pd.to_datetime(df.get("fecha"), errors="coerce")
    if "descripcion" not in df.columns:
        df["descripcion"] = ""
    df["descripcion"] = df["descripcion"].astype(str).str.strip()
    return df[["fecha", "referencia", "descripcion", "valor"]]


def agrupar(df: pd.DataFrame, sufijo: str) -> pd.DataFrame:
    g = (df.groupby("referencia")
         .agg(**{f"fecha_{sufijo}": ("fecha", "min"),
                 f"descripcion_{sufijo}": ("descripcion", "first"),
                 f"valor_{sufijo}": ("valor", "sum")})
         .reset_index())
    g[f"valor_{sufijo}"] = g[f"valor_{sufijo}"].round(2)
    return g


def cruce_por_valor(pendientes_libros: pd.DataFrame, pendientes_extracto: pd.DataFrame,
                    dias: int) -> list[tuple[str, str]]:
    """Empareja por valor identico y fecha cercana. Devuelve pares (ref_libros, ref_extracto)."""
    pares, usados = [], set()
    for _, l in pendientes_libros.iterrows():
        cand = pendientes_extracto[
            (~pendientes_extracto["referencia"].isin(usados))
            & (pendientes_extracto["valor_extracto"] == l["valor_libros"])
        ]
        if l["fecha_libros"] is not pd.NaT and cand["fecha_extracto"].notna().any():
            cand = cand[(cand["fecha_extracto"] - l["fecha_libros"]).abs()
                        <= pd.Timedelta(days=dias)]
        if len(cand):
            ref_e = cand.iloc[0]["referencia"]
            usados.add(ref_e)
            pares.append((l["referencia"], ref_e))
    return pares


def main() -> None:
    ap = argparse.ArgumentParser(description="Conciliacion bancaria automatizada")
    ap.add_argument("libros")
    ap.add_argument("extracto")
    ap.add_argument("--saldo-inicial", type=float, default=0.0,
                    help="Saldo inicial comun a libros y extracto")
    ap.add_argument("--dias", type=int, default=5,
                    help="Tolerancia en dias para el cruce por valor")
    ap.add_argument("--salida", default="salidas/conciliacion_bancaria.xlsx")
    args = ap.parse_args()

    lib = cargar(Path(args.libros), "LIBROS")
    ext = cargar(Path(args.extracto), "EXTRACTO")

    gl, ge = agrupar(lib, "libros"), agrupar(ext, "extracto")
    conc = gl.merge(ge, on="referencia", how="outer", indicator=True)

    # --- segundo cruce: por valor y fecha cercana, sobre lo que quedo sin pareja
    solo_l = conc[conc["_merge"] == "left_only"]
    solo_e = conc[conc["_merge"] == "right_only"]
    pares = cruce_por_valor(solo_l, solo_e, args.dias)
    for ref_l, ref_e in pares:
        fila_e = conc.loc[conc["referencia"] == ref_e].iloc[0]
        i = conc.index[conc["referencia"] == ref_l][0]
        conc.loc[i, ["fecha_extracto", "descripcion_extracto", "valor_extracto"]] = [
            fila_e["fecha_extracto"], fila_e["descripcion_extracto"], fila_e["valor_extracto"]]
        conc.loc[i, "_merge"] = "both"
        conc.loc[i, "cruce"] = f"POR VALOR (ref. banco {ref_e})"
        conc = conc[conc["referencia"] != ref_e]

    conc[["valor_libros", "valor_extracto"]] = conc[["valor_libros", "valor_extracto"]].fillna(0.0)
    conc["diferencia"] = (conc["valor_libros"] - conc["valor_extracto"]).round(2)
    if "cruce" not in conc.columns:
        conc["cruce"] = "POR REFERENCIA"
    conc["cruce"] = conc["cruce"].fillna("POR REFERENCIA")

    conc["situacion"] = conc["_merge"].map({
        "both": "CONCILIADA",
        "left_only": "SOLO EN LIBROS (partida en transito)",
        "right_only": "SOLO EN EXTRACTO (registrar en libros)",
    }).astype(str)
    conc.loc[(conc["_merge"] == "both") & (conc["diferencia"] != 0),
             "situacion"] = "DIFERENCIA DE VALOR"

    # ------------------------------------------------------- prueba de saldos
    solo_libros = conc.loc[conc["situacion"].str.startswith("SOLO EN LIBROS"), "valor_libros"].sum()
    solo_extracto = conc.loc[conc["situacion"].str.startswith("SOLO EN EXTRACTO"), "valor_extracto"].sum()
    dif_valor = conc.loc[conc["situacion"] == "DIFERENCIA DE VALOR", "diferencia"].sum()

    saldo_libros = round(args.saldo_inicial + lib["valor"].sum(), 2)
    saldo_extracto = round(args.saldo_inicial + ext["valor"].sum(), 2)
    saldo_conciliado = round(saldo_extracto + solo_libros - solo_extracto + dif_valor, 2)
    descuadre = round(saldo_conciliado - saldo_libros, 2)

    resumen = pd.DataFrame({
        "concepto": [
            "Saldo segun extracto bancario",
            "(+) Partidas registradas en libros y no en el banco",
            "(-) Partidas del banco no registradas en libros",
            "(+/-) Diferencias de valor",
            "(=) Saldo conciliado",
            "Saldo segun libros",
            "Descuadre",
        ],
        "valor": [saldo_extracto, solo_libros, -solo_extracto, dif_valor,
                  saldo_conciliado, saldo_libros, descuadre],
    })

    partidas = conc[conc["situacion"] != "CONCILIADA"].drop(columns="_merge")
    partidas = partidas.sort_values(["situacion", "valor_libros"], ascending=[True, False])

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(salida, engine="openpyxl") as w:
        resumen.to_excel(w, sheet_name="Resumen", index=False)
        partidas.to_excel(w, sheet_name="Partidas conciliatorias", index=False)
        conc.drop(columns="_merge").to_excel(w, sheet_name="Detalle del cruce", index=False)

    print(conc["situacion"].value_counts().to_string(), "\n")
    for _, r in resumen.iterrows():
        print(f"{r['concepto']:<52} {r['valor']:>18,.2f}")
    print()
    print("CONCILIACION OK" if descuadre == 0
          else f"REVISAR: quedan {descuadre:,.2f} sin explicar")
    print(f"Archivo generado: {salida}")


if __name__ == "__main__":
    main()
