"""
Procesa un archivo de facturas de proveedores y calcula las retenciones de cada una.

    python procesar_lote.py facturas.csv
    python procesar_lote.py facturas.xlsx --salida retenciones_marzo.xlsx

Columnas que reconoce el archivo de entrada (los nombres se normalizan a minusculas
y sin tildes; las columnas que falten toman el valor por defecto):

    numero_factura, fecha, nit, proveedor, concepto, base_gravable, iva,
    declarante (SI/NO), gran_contribuyente (SI/NO), autorretenedor (SI/NO),
    regimen_simple (SI/NO), actividad_ica

Salida: un Excel con tres hojas -> Detalle, Resumen por proveedor, Resumen por concepto.
"""
from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import pandas as pd

from retenciones import Calculadora


def normalizar(col: str) -> str:
    s = unicodedata.normalize("NFKD", str(col)).encode("ascii", "ignore").decode()
    return s.strip().lower().replace(" ", "_")


def a_bool(valor, por_defecto=False) -> bool:
    if pd.isna(valor):
        return por_defecto
    return str(valor).strip().upper() in {"SI", "SÍ", "S", "TRUE", "1", "X", "YES"}


def leer(ruta: Path) -> pd.DataFrame:
    if ruta.suffix.lower() in {".xlsx", ".xlsm", ".xls"}:
        df = pd.read_excel(ruta, dtype={"nit": str})
    else:
        df = pd.read_csv(ruta, dtype={"nit": str}, sep=None, engine="python")
    df.columns = [normalizar(c) for c in df.columns]
    return df


def main() -> None:
    ap = argparse.ArgumentParser(description="Calculo masivo de retenciones")
    ap.add_argument("entrada", help="CSV o Excel con las facturas")
    ap.add_argument("--salida", default="salidas/retenciones_calculadas.xlsx")
    ap.add_argument("--tarifas", default=None, help="Ruta alterna al JSON de tarifas")
    args = ap.parse_args()

    calc = Calculadora(args.tarifas) if args.tarifas else Calculadora()
    df = leer(Path(args.entrada))

    if "base_gravable" not in df.columns:
        raise SystemExit("El archivo debe traer al menos la columna 'base_gravable'.")

    filas = []
    for _, f in df.iterrows():
        res = calc.calcular(
            base_gravable=float(f["base_gravable"]),
            concepto=str(f.get("concepto", "compras_generales_declarante")).strip(),
            iva=float(f["iva"]) if "iva" in df.columns and not pd.isna(f.get("iva")) else None,
            proveedor_es_declarante=a_bool(f.get("declarante"), True),
            gran_contribuyente=a_bool(f.get("gran_contribuyente")),
            autorretenedor=a_bool(f.get("autorretenedor")),
            regimen_simple=a_bool(f.get("regimen_simple")),
            actividad_ica=(None if pd.isna(f.get("actividad_ica")) else str(f.get("actividad_ica"))),
        )
        fila = {
            "numero_factura": f.get("numero_factura"),
            "fecha": f.get("fecha"),
            "nit": f.get("nit"),
            "proveedor": f.get("proveedor"),
        }
        fila.update(res.to_dict())
        filas.append(fila)

    det = pd.DataFrame(filas)

    por_proveedor = (det.groupby(["nit", "proveedor"], dropna=False)
                     [["base_gravable", "iva", "retefuente", "reteiva", "reteica", "neto_a_pagar"]]
                     .sum().round(2).reset_index()
                     .sort_values("base_gravable", ascending=False))
    por_concepto = (det.groupby("descripcion_concepto")
                    [["base_gravable", "retefuente", "reteiva", "reteica"]]
                    .agg(["count", "sum"]).round(2))

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(salida, engine="openpyxl") as w:
        det.to_excel(w, sheet_name="Detalle", index=False)
        por_proveedor.to_excel(w, sheet_name="Por proveedor", index=False)
        por_concepto.to_excel(w, sheet_name="Por concepto")

    print(f"Facturas procesadas : {len(det)}")
    print(f"Base gravable total : {det['base_gravable'].sum():>16,.2f}")
    print(f"Retefuente          : {det['retefuente'].sum():>16,.2f}")
    print(f"ReteIVA             : {det['reteiva'].sum():>16,.2f}")
    print(f"ReteICA             : {det['reteica'].sum():>16,.2f}")
    print(f"Neto a pagar        : {det['neto_a_pagar'].sum():>16,.2f}")
    alertas = det[det["observaciones"].str.len() > 0]
    if len(alertas):
        print(f"\nFacturas con observacion: {len(alertas)} (revise la hoja Detalle)")
    print(f"\nArchivo generado: {salida}")


if __name__ == "__main__":
    main()
