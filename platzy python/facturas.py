import glob
import re
import pandas as pd
import pdfplumber


def a_float(val):
    if not val:
        return 0.0
    return float(val.replace(".", "").replace(",", "."))


def extraer_datos_factura(ruta_pdf):
    texto_completo = ""
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            t = pagina.extract_text()
            if t:
                texto_completo += t + "\n"

    # 1. Extraer IBUA
    match_ibua = re.search(r"IBUA\s+([\d\.,]+)", texto_completo)
    val_ibua = a_float(match_ibua.group(1)) if match_ibua else 0.0

    # 2. Capturar ítems buscando el patrón por bloque numérico final
    # Estrategia: Buscar líneas que inicien con: Nro + Código
    patron_bloque = re.compile(
        r"(\d+)\s+(\d+)\s+(.+?)\s+([A-Z]{2})\s+([\d\.,]+)\s+\$\s*([\d\.,]+)\s+\$\s*([\d\.,]+)\s+\$\s*([\d\.,]+)\s+\$\s*([\d\.,]+)\s+([\d\.,]+)\s+\$\s*([\d\.,]+)"
    )

    # Limpiamos saltos de línea que parten descripciones
    texto_limpio = re.sub(r"\n(?!\d+\s+\d+\s+)", " ", texto_completo)

    items = []
    for match in patron_bloque.finditer(texto_limpio):
        (
            nro,
            cod,
            desc,
            um,
            cant,
            p_unit,
            desc_val,
            recargo,
            iva_val,
            iva_pct,
            p_venta,
        ) = match.groups()

        items.append(
            {
                "Item": int(nro),
                "Código": cod,
                "Descripción": re.sub(r"\s+", " ", desc).strip(),
                "Unidad": um,
                "Cantidad": a_float(cant),
                "Precio_Unitario": a_float(p_unit),
                "Descuento": a_float(desc_val),
                "IVA_Valor": a_float(iva_val),
                "IVA_Pct": a_float(iva_pct),
                "Subtotal_Neto": a_float(p_venta),
            }
        )

    df_items = pd.DataFrame(items)

    if df_items.empty:
        raise ValueError(
            "No se logró estructurar la tabla de productos del PDF."
        )

    # 3. Clasificación PUC e IBUA Prorrateado al Costo de Inventario
    df_items["Cuenta_PUC"] = df_items["IVA_Pct"].apply(
        lambda x: "14350501" if x == 19.0 else "14350502"
    )

    mask_gravado = df_items["Cuenta_PUC"] == "14350501"
    subtotal_gravado = df_items.loc[mask_gravado, "Subtotal_Neto"].sum()

    if val_ibua > 0 and subtotal_gravado > 0:
        df_items["IBUA_Prorrateado"] = 0.0
        df_items.loc[mask_gravado, "IBUA_Prorrateado"] = (
            df_items.loc[mask_gravado, "Subtotal_Neto"] / subtotal_gravado
        ) * val_ibua
    else:
        df_items["IBUA_Prorrateado"] = 0.0

    df_items["Costo_Total_Inventario"] = (
        df_items["Subtotal_Neto"] + df_items["IBUA_Prorrateado"]
    )

    return df_items, val_ibua


if __name__ == "__main__":
    archivos_pdf = glob.glob("*.pdf")

    if not archivos_pdf:
        print("❌ No hay archivos PDF en la carpeta.")
    else:
        pdf_target = archivos_pdf[0]
        print(f"📄 Procesando factura: {pdf_target}")

        df_factura, ibua_total = extraer_datos_factura(pdf_target)

        ruta_salida = "Factura_Procesada.xlsx"
        with pd.ExcelWriter(ruta_salida, engine="openpyxl") as writer:
            df_factura.to_excel(
                writer, sheet_name="Detalle_Productos", index=False
            )

        print(
            f"✅ ¡Proceso completado con éxito! Se exportó '{ruta_salida}' con {len(df_factura)} registros."
        )