"""
PLANTILLA REUTILIZABLE - analisis rapido de cualquier archivo contable.

Copia este archivo, cambia RUTA y las funciones que necesites. Esta escrito como
una caja de herramientas: cada funcion hace una sola cosa y puedes llamarlas sueltas.

    python plantilla_analisis_contable.py archivo.csv
    python plantilla_analisis_contable.py archivo.xlsx --columna-valor debito
"""
from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import pandas as pd

pd.set_option("display.float_format", lambda x: f"{x:,.2f}")
pd.set_option("display.max_columns", 40)
pd.set_option("display.width", 160)


# --------------------------------------------------------------- 1. cargar
def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """quita tildes, espacios y mayusculas de los nombres de columna"""
    def limpiar(c):
        s = unicodedata.normalize("NFKD", str(c)).encode("ascii", "ignore").decode()
        return s.strip().lower().replace(" ", "_").replace(".", "")
    df.columns = [limpiar(c) for c in df.columns]
    return df


def cargar(ruta: str | Path, **kwargs) -> pd.DataFrame:
    """lee csv, xlsx o txt y normaliza los nombres de columna"""
    ruta = Path(ruta)
    if ruta.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        df = pd.read_excel(ruta, **kwargs)
    else:
        df = pd.read_csv(ruta, sep=None, engine="python", **kwargs)
    return normalizar_columnas(df)


# ------------------------------------------------------------ 2. explorar
def perfil(df: pd.DataFrame) -> pd.DataFrame:
    """una fila por columna: tipo, nulos, unicos y un valor de ejemplo"""
    return pd.DataFrame({
        "tipo": df.dtypes.astype(str),
        "nulos": df.isna().sum(),
        "%_nulos": (df.isna().mean() * 100).round(1),
        "unicos": df.nunique(),
        "ejemplo": [df[c].dropna().iloc[0] if df[c].notna().any() else None for c in df.columns],
    })


def diagnostico(df: pd.DataFrame) -> None:
    print(f"Filas: {len(df):,}  |  Columnas: {df.shape[1]}")
    print(f"Duplicados exactos: {df.duplicated().sum():,}")
    print(f"Memoria: {df.memory_usage(deep=True).sum() / 1e6:,.1f} MB\n")
    print(perfil(df).to_string())


# ------------------------------------------------------------- 3. limpiar
def limpiar_texto(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    for c in columnas:
        if c in df.columns:
            df[c] = df[c].astype(str).str.strip().str.upper().replace({"NAN": None})
    return df


def a_numero(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """convierte texto con separadores de miles a numero: '1.234.567,89' -> 1234567.89"""
    for c in columnas:
        if c in df.columns and df[c].dtype == object:
            df[c] = (df[c].astype(str)
                     .str.replace(r"[$\s]", "", regex=True)
                     .str.replace(".", "", regex=False)
                     .str.replace(",", ".", regex=False))
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)
    return df


def a_fecha(df: pd.DataFrame, columnas: list[str], formato: str | None = None) -> pd.DataFrame:
    """Convierte a fecha. Detecta el formato ISO (2026-03-05) para no confundir dia y mes;
    para el resto asume el formato colombiano dd/mm/aaaa."""
    for c in columnas:
        if c not in df.columns:
            continue
        if formato:
            df[c] = pd.to_datetime(df[c], format=formato, errors="coerce")
            continue
        muestra = df[c].astype(str).head(50)
        es_iso = muestra.str.match(r"^\d{4}-\d{2}-\d{2}").mean() > 0.8
        df[c] = pd.to_datetime(df[c], errors="coerce", dayfirst=not es_iso)
    return df


# ------------------------------------------------------------ 4. analizar
def resumen_por(df: pd.DataFrame, agrupar: str, valor: str, top: int = 10) -> pd.DataFrame:
    """total, conteo, promedio y participacion por categoria"""
    r = (df.groupby(agrupar)[valor]
         .agg(total="sum", movimientos="count", promedio="mean")
         .sort_values("total", ascending=False))
    r["participacion_%"] = (r["total"] / r["total"].sum() * 100).round(2)
    r["acumulado_%"] = r["participacion_%"].cumsum().round(2)
    return r.head(top).round(2)


def serie_mensual(df: pd.DataFrame, fecha: str, valor: str) -> pd.DataFrame:
    """total por mes con variacion absoluta y porcentual"""
    s = (df.assign(mes=df[fecha].dt.to_period("M"))
         .groupby("mes")[valor].sum().to_frame("total"))
    s["variacion"] = s["total"].diff().round(2)
    s["variacion_%"] = (s["total"].pct_change() * 100).round(2)
    return s.round(2)


def edades(df: pd.DataFrame, fecha: str, valor: str, corte=None,
           cortes=(0, 30, 60, 90, 180, 360, 99999)) -> pd.DataFrame:
    """clasifica saldos por antiguedad - util para cartera y proveedores"""
    corte = pd.Timestamp(corte) if corte else pd.Timestamp.today()
    d = df.copy()
    d["dias"] = (corte - d[fecha]).dt.days
    etiquetas = ["0-30", "31-60", "61-90", "91-180", "181-360", "+360"]
    d["rango"] = pd.cut(d["dias"], bins=cortes, labels=etiquetas, right=True)
    r = d.groupby("rango", observed=False)[valor].agg(saldo="sum", documentos="count")
    r["participacion_%"] = (r["saldo"] / r["saldo"].sum() * 100).round(2)
    return r.round(2)


def pareto(df: pd.DataFrame, agrupar: str, valor: str, umbral: float = 80.0) -> pd.DataFrame:
    """devuelve las categorias que explican el umbral% del total (regla 80/20)"""
    r = resumen_por(df, agrupar, valor, top=10_000)
    return r[r["acumulado_%"] <= umbral]


# ------------------------------------------------------------ 5. exportar
def exportar(hojas: dict[str, pd.DataFrame], ruta: str | Path) -> Path:
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(ruta, engine="openpyxl") as w:
        for nombre, tabla in hojas.items():
            tabla.to_excel(w, sheet_name=nombre[:31])
    print(f"Archivo generado: {ruta}")
    return ruta


# --------------------------------------------------------------- ejemplo
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--columna-valor", default=None)
    ap.add_argument("--columna-fecha", default=None)
    ap.add_argument("--agrupar-por", default=None)
    args = ap.parse_args()

    df = cargar(args.archivo)
    print("=" * 80, "\nDIAGNOSTICO\n" + "=" * 80)
    diagnostico(df)

    valor = args.columna_valor or next(
        (c for c in ("valor", "debito", "saldo_final", "total") if c in df.columns), None)
    fecha = args.columna_fecha or next((c for c in ("fecha", "fecha_factura") if c in df.columns), None)

    if valor:
        df = a_numero(df, [valor])
        if fecha:
            df = a_fecha(df, [fecha])
            print("\n" + "=" * 80, "\nSERIE MENSUAL\n" + "=" * 80)
            print(serie_mensual(df, fecha, valor).to_string())
        agrupar = args.agrupar_por or next(
            (c for c in df.columns if df[c].dtype == object and 2 < df[c].nunique() < 60), None)
        if agrupar:
            print("\n" + "=" * 80, f"\nRESUMEN POR {agrupar.upper()}\n" + "=" * 80)
            print(resumen_por(df, agrupar, valor).to_string())
