"""
Prepara el formato 1001 de informacion exogena (pagos o abonos en cuenta y
retenciones practicadas) a partir del libro auxiliar contable.

    python generar_1001.py libro_auxiliar.csv --anio 2026

Que hace
--------
1. Clasifica cada movimiento por concepto 1001 segun el prefijo de la cuenta PUC
   (mapeo editable en conceptos_1001.json).
2. Acumula por tercero + concepto el pago o abono en cuenta.
3. Cruza las retenciones practicadas (cuentas 2365 / 2367 / 2368) por tercero.
4. Marca los terceros que no superan el tope y deben ir en la cuantia menor
   (NIT 222222222).
5. Exporta un Excel con la estructura del formato y una hoja de control.

El archivo de entrada necesita: fecha, codigo_puc, nit_tercero, nombre_tercero,
debito, credito. Nombres alternos comunes se reconocen automaticamente.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

CFG = json.loads(Path(__file__).with_name("conceptos_1001.json").read_text(encoding="utf-8"))

ALIAS = {
    "cuenta": "codigo_puc", "codigo_cuenta": "codigo_puc", "puc": "codigo_puc",
    "nit": "nit_tercero", "identificacion": "nit_tercero", "tercero": "nit_tercero",
    "nombre": "nombre_tercero", "razon_social": "nombre_tercero",
    "debe": "debito", "haber": "credito",
}


def concepto_de(cuenta: str) -> tuple[str, str] | tuple[None, None]:
    for prefijo, info in CFG["mapeo_puc_concepto"].items():
        if str(cuenta).startswith(prefijo):
            return info["concepto"], info["nombre"]
    return None, None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("auxiliar", help="CSV o Excel del libro auxiliar")
    ap.add_argument("--anio", type=int, default=None, help="Filtrar por ano gravable")
    ap.add_argument("--salida", default="salidas/formato_1001.xlsx")
    ap.add_argument("--tope", type=float, default=None, help="Tope minimo por tercero")
    args = ap.parse_args()

    ruta = Path(args.auxiliar)
    df = (pd.read_excel(ruta, dtype=str) if ruta.suffix.lower().startswith(".xls")
          else pd.read_csv(ruta, dtype=str))
    df.columns = [ALIAS.get(c.strip().lower(), c.strip().lower()) for c in df.columns]

    faltan = {"codigo_puc", "nit_tercero", "debito", "credito"} - set(df.columns)
    if faltan:
        raise SystemExit(f"Faltan columnas en el auxiliar: {sorted(faltan)}")

    for c in ("debito", "credito"):
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    if "fecha" in df.columns:
        df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")
        if args.anio:
            df = df[df["fecha"].dt.year == args.anio]
    if "nombre_tercero" not in df.columns:
        df["nombre_tercero"] = ""

    # ------------------------------------------------ pagos o abonos en cuenta
    df[["concepto", "nombre_concepto"]] = df["codigo_puc"].apply(
        lambda c: pd.Series(concepto_de(c)))
    pagos = df[df["concepto"].notna()].copy()
    pagos["valor"] = pagos["debito"] - pagos["credito"]

    base = (pagos.groupby(["nit_tercero", "nombre_tercero", "concepto", "nombre_concepto"],
                          dropna=False)["valor"].sum().round(0).reset_index()
            .rename(columns={"valor": "pago_o_abono_en_cuenta"}))
    base = base[base["pago_o_abono_en_cuenta"] > 0]

    # ------------------------------------------------------------ retenciones
    ctas = CFG["cuentas_retencion"]
    ret = {}
    for etiqueta, prefijo in ctas.items():
        sub = df[df["codigo_puc"].str.startswith(prefijo)].copy()
        sub["valor_retenido"] = sub["credito"] - sub["debito"]
        ret[etiqueta] = sub.groupby("nit_tercero")["valor_retenido"].sum().round(0)
    for etiqueta, serie in ret.items():
        base[etiqueta] = base["nit_tercero"].map(serie).fillna(0.0)

    # ------------------------------------------------------ cuantias menores
    tope = args.tope if args.tope is not None else CFG["topes"]["tope_general_por_tercero"]
    base["supera_tope"] = base["pago_o_abono_en_cuenta"] >= tope

    menores = base[~base["supera_tope"]].copy()
    if len(menores):
        agrupado = (menores.groupby(["concepto", "nombre_concepto"], as_index=False)
                    .agg({"pago_o_abono_en_cuenta": "sum",
                          "retencion_renta": "sum",
                          "retencion_iva": "sum",
                          "retencion_ica": "sum"}))
        agrupado["nit_tercero"] = "222222222"
        agrupado["nombre_tercero"] = "CUANTIAS MENORES"
        agrupado["supera_tope"] = True
        formato = pd.concat([base[base["supera_tope"]], agrupado], ignore_index=True)
    else:
        formato = base[base["supera_tope"]].copy()

    formato = formato[[
        "concepto", "nombre_concepto", "nit_tercero", "nombre_tercero",
        "pago_o_abono_en_cuenta", "retencion_renta", "retencion_iva", "retencion_ica",
    ]].sort_values(["concepto", "pago_o_abono_en_cuenta"], ascending=[True, False])

    # ------------------------------------------------------------- controles
    sin_mapear = (df[df["concepto"].isna() & df["codigo_puc"].str.startswith(("5", "6"))]
                  .groupby("codigo_puc")[["debito"]].sum().reset_index()
                  .rename(columns={"debito": "valor_no_clasificado"})
                  .sort_values("valor_no_clasificado", ascending=False))

    control = pd.DataFrame({
        "concepto_control": [
            "Terceros reportados", "Terceros en cuantias menores",
            "Total pagos reportados", "Total retencion renta",
            "Total retencion IVA", "Total retencion ICA",
            "Cuentas 5x/6x sin concepto asignado", "Tope aplicado por tercero",
        ],
        "valor": [
            formato["nit_tercero"].nunique(), len(menores),
            round(formato["pago_o_abono_en_cuenta"].sum(), 0),
            round(formato["retencion_renta"].sum(), 0),
            round(formato["retencion_iva"].sum(), 0),
            round(formato["retencion_ica"].sum(), 0),
            len(sin_mapear), tope,
        ],
    })

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(salida, engine="openpyxl") as w:
        formato.to_excel(w, sheet_name="Formato 1001", index=False)
        control.to_excel(w, sheet_name="Control", index=False)
        sin_mapear.to_excel(w, sheet_name="Cuentas sin concepto", index=False)

    print(control.to_string(index=False))
    if len(sin_mapear):
        print(f"\nATENCION: {len(sin_mapear)} cuentas de gasto/costo sin concepto 1001. "
              "Agreguelas a conceptos_1001.json antes de presentar.")
    print(f"\nArchivo generado: {salida}")


if __name__ == "__main__":
    main()
