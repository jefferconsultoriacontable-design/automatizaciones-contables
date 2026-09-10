import openpyxl
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation


def crear_checklist_empalme():
    wb = openpyxl.Workbook()

    # ---------------------------------------------------------
    # HOJA 1: CHECKLIST DE EMPALME
    # ---------------------------------------------------------
    ws = wb.active
    ws.title = "Checklist Empalme"
    ws.views.sheetView[0].showGridLines = True

    # Colores base
    NAVY = "1F4E79"
    WHITE = "FFFFFF"
    LIGHT_GRAY = "F2F2F2"
    BORDER_COLOR = "D9D9D9"

    # Estilos
    font_title = Font(name="Calibri", size=14, bold=True, color=WHITE)
    font_header = Font(name="Calibri", size=11, bold=True, color=WHITE)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)

    fill_navy = PatternFill(
        start_color=NAVY, end_color=NAVY, fill_type="solid"
    )
    fill_light = PatternFill(
        start_color=LIGHT_GRAY, end_color=LIGHT_GRAY, fill_type="solid"
    )

    thin_border = Side(style="thin", color=BORDER_COLOR)
    border_all = Border(
        left=thin_border, right=thin_border, top=thin_border, bottom=thin_border
    )

    # 1. ENCABEZADO DE LA EMPRESA
    ws.merge_cells("A1:G1")
    ws["A1"] = "EMPALME CONTABLE - INGENIO VERDE INGEV S.A.S. (NIT: 901.166.067-4)"
    ws["A1"].font = font_title
    ws["A1"].fill = fill_navy
    ws["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 35

    ws["A2"] = "Firma Saliente:"
    ws["B2"] = "TAX PAY S.A.S."
    ws["D2"] = "Fecha Empalme:"
    ws["E2"] = "27/08/2026"

    ws["A3"] = "Ubicación:"
    ws["B3"] = "Yopal, Casanare"
    ws["D3"] = "Contador Entrante:"
    ws["E3"] = "Jeffer Daniel Pacheco Peña"

    for row in range(2, 4):
        ws[f"A{row}"].font = font_bold
        ws[f"D{row}"].font = font_bold
        ws[f"B{row}"].font = font_regular
        ws[f"E{row}"].font = font_regular

    # 2. CUADRO DE RESUMEN / DASHBOARD
    ws.merge_cells("F2:G2")
    ws["F2"] = "RESUMEN DE RECEPCIÓ N"
    ws["F2"].font = font_header
    ws["F2"].fill = fill_navy
    ws["F2"].alignment = Alignment(horizontal="center", vertical="center")

    resumen_items = [
        ("RECIBIDO", '=COUNTIF(E8:E30, "RECIBIDO")', "C6EFCE", "006100"),
        ("PENDIENTE", '=COUNTIF(E8:E30, "PENDIENTE")', "FFC7CE", "9C0006"),
        ("EN PROCESO", '=COUNTIF(E8:E30, "EN PROCESO")', "FFEB9C", "9C6500"),
        ("NO APLICA", '=COUNTIF(E8:E30, "NO APLICA")', "E2EFDA", "375623"),
    ]

    for idx, (estado, formula, bg_color, font_color) in enumerate(
        resumen_items, start=3
    ):
        ws[f"F{idx}"] = estado
        ws[f"G{idx}"] = formula

        ws[f"F{idx}"].font = Font(name="Calibri", size=10, bold=True)
        ws[f"G{idx}"].font = Font(
            name="Calibri", size=10, bold=True, color=font_color
        )

        ws[f"F{idx}"].fill = PatternFill(
            start_color=bg_color, end_color=bg_color, fill_type="solid"
        )
        ws[f"G{idx}"].fill = PatternFill(
            start_color=bg_color, end_color=bg_color, fill_type="solid"
        )

        ws[f"F{idx}"].border = border_all
        ws[f"G{idx}"].border = border_all
        ws[f"G{idx}"].alignment = Alignment(horizontal="center")

    # 3. TABLA PRINCIPAL DE CHECKLIST
    headers = [
        "Item",
        "Categoría / Área",
        "Requerimiento Solicitado (Según Comunicación)",
        "Responsable Delivery",
        "Estado",
        "Observaciones / Soportes Entregados",
        "Fecha Compromiso",
    ]

    start_row = 7
    ws.row_dimensions[start_row].height = 25

    for col_num, header_title in enumerate(headers, 1):
        cell = ws.cell(row=start_row, column=col_num)
        cell.value = header_title
        cell.font = font_header
        cell.fill = fill_navy
        cell.alignment = Alignment(
            horizontal="center", vertical="center", wrap_text=True
        )
        cell.border = border_all

    # Datos basados exactamente en tus 23 puntos
    puntos_carta = [
        (
            1,
            "Soportes y Archivo",
            "Causaciones de compras, impuestos, egresos, recibos de caja, pagos y trazabilidad documental (DSNO, seguridad social).",
        ),
        (
            2,
            "Tesorería / Caja",
            "Conciliación de caja general/menor, concordancia con la realidad económica y evidencia de arqueos.",
        ),
        (
            3,
            "Bancos",
            "Relación de cuentas bancarias y conciliaciones bancarias mensuales debidamente soportadas.",
        ),
        (
            4,
            "Activos Fijos",
            "Relación de activos fijos en Excel (cuenta, detalle, serie, compra, proveedor, depreciación mensual, vida útil, acum).",
        ),
        (
            5,
            "Cartera / CxC",
            "Relación detallada de cuentas por cobrar a clientes clasificada por rangos de vencimiento.",
        ),
        (
            6,
            "Cartera / Provisión",
            "Informe de CxC de difícil cobro, provisión de cartera registrada y políticas aplicadas.",
        ),
        (
            7,
            "Diferidos",
            "Detalle de cargos diferidos, amortización mensual y fecha de finalización.",
        ),
        (
            8,
            "Inventarios / Proyectos",
            "Relación de inventarios por proyecto, % de avance de ejecución y método de determinación de costos.",
        ),
        (
            9,
            "Inventarios / Deterioro",
            "Informe de inventario deteriorado (obsolescencia, daño, baja rotación), medición y registros.",
        ),
        (
            10,
            "Inversiones",
            "Relación de inversiones (Acciones, Fiducias, CDTs, participaciones en negocios conjuntos, etc.).",
        ),
        (
            11,
            "Pasivos / CxP",
            "Relación detallada de cuentas por pagar a proveedores ordenadas por rangos de vencimiento.",
        ),
        (
            12,
            "Facturación Electrónica",
            "Estado del proceso de acuse de recibo para compras a crédito (trazabilidad RADIAN) y proveedores.",
        ),
        (
            13,
            "Impuestos Pendientes",
            "Relación de impuestos pendientes por pagar (Nacionales, Municipales y Distritales).",
        ),
        (
            14,
            "Obligaciones Financieras",
            "Relación de créditos bancarios con sus amortizaciones debidamente conciliadas.",
        ),
        (
            15,
            "Nómina y N. Electrónica",
            "Estado de nómina, personal por liquidar, transmisión de Nómina Electrónica y política de provisiones.",
        ),
        (
            16,
            "Facturación e Ingresos",
            "Relación de ingresos pendientes por facturar detallados por cada proyecto y municipio.",
        ),
        (
            17,
            "Impuestos Municipales",
            "Municipios con ICA, periodicidad, forma de presentación y credenciales de acceso a portales web.",
        ),
        (
            18,
            "Declaraciones Tributarias",
            "Archivo digital de declaraciones (presentadas, pago y anexos/auxiliares en Excel/PDF).",
        ),
        (
            19,
            "Históricos y Exógena",
            "Histórico de exógena (nacional/municipal), declaraciones años anteriores, EEFF y conciliación fiscal (F. 2516).",
        ),
        (
            20,
            "Estados Financieros",
            "Estados Financieros certificados con sus respectivas notas de revelación al cierre de 2025.",
        ),
        (
            21,
            "Fiscalización DIAN/Municipios",
            "Informe sobre procesos de fiscalización, requerimientos o requerimientos especiales en curso.",
        ),
        (
            22,
            "Políticas Contables",
            "Manual formal de Políticas Contables bajo NIIF adoptado por la empresa.",
        ),
        (
            23,
            "Información Adicional",
            "Entrega de cualquier otra información o aspecto relevante que infiera en los procesos o toma de decisiones.",
        ),
    ]

    current_row = 8
    for item_num, cat, desc in puntos_carta:
        ws.cell(row=current_row, column=1, value=item_num).alignment = (
            Alignment(horizontal="center", vertical="top")
        )
        ws.cell(row=current_row, column=2, value=cat).alignment = Alignment(
            vertical="top"
        )
        ws.cell(row=current_row, column=3, value=desc).alignment = Alignment(
            wrap_text=True, vertical="top"
        )
        ws.cell(row=current_row, column=4, value="TAX PAY").alignment = (
            Alignment(horizontal="center", vertical="top")
        )

        # Estado por defecto
        cell_estado = ws.cell(row=current_row, column=5, value="PENDIENTE")
        cell_estado.alignment = Alignment(
            horizontal="center", vertical="top"
        )

        ws.cell(row=current_row, column=6, value="").alignment = Alignment(
            wrap_text=True, vertical="top"
        )
        ws.cell(row=current_row, column=7, value="").alignment = Alignment(
            horizontal="center", vertical="top"
        )

        # Formato de bordes y fuentes
        for c in range(1, 8):
            cell = ws.cell(row=current_row, column=c)
            cell.font = font_regular
            cell.border = border_all

        # Aplicar sombreado intercalado claro
        if item_num % 2 == 0:
            for c in range(1, 8):
                ws.cell(row=current_row, column=c).fill = fill_light

        ws.row_dimensions[current_row].height = 32
        current_row += 1

    # 4. VALIDACIÓN DE DATOS (Lista Desplegable en Estado)
    dv = DataValidation(
        type="list",
        formula1='"RECIBIDO,PENDIENTE,EN PROCESO,NO APLICA"',
        allow_blank=True,
    )
    ws.add_data_validation(dv)
    dv.add(f"E8:E{current_row-1}")

    # 5. FORMATO CONDICIONAL PARA ESTADOS
    green_fill = PatternFill(
        start_color="C6EFCE", end_color="C6EFCE", fill_type="solid"
    )
    red_fill = PatternFill(
        start_color="FFC7CE", end_color="FFC7CE", fill_type="solid"
    )
    yellow_fill = PatternFill(
        start_color="FFEB9C", end_color="FFEB9C", fill_type="solid"
    )
    gray_fill = PatternFill(
        start_color="E2EFDA", end_color="E2EFDA", fill_type="solid"
    )

    ws.conditional_formatting.add(
        f"E8:E{current_row-1}",
        CellIsRule(operator="equal", formula=['"RECIBIDO"'], fill=green_fill),
    )
    ws.conditional_formatting.add(
        f"E8:E{current_row-1}",
        CellIsRule(operator="equal", formula=['"PENDIENTE"'], fill=red_fill),
    )
    ws.conditional_formatting.add(
        f"E8:E{current_row-1}",
        CellIsRule(operator="equal", formula=['"EN PROCESO"'], fill=yellow_fill),
    )
    ws.conditional_formatting.add(
        f"E8:E{current_row-1}",
        CellIsRule(operator="equal", formula=['"NO APLICA"'], fill=gray_fill),
    )

    # Ajustar anchos de columna
    col_widths = {
        "A": 7,
        "B": 22,
        "C": 48,
        "D": 16,
        "E": 15,
        "F": 35,
        "G": 18,
    }
    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    # ---------------------------------------------------------
    # HOJA 2: ACTA DE EMPALME Y FIRMAS
    # ---------------------------------------------------------
    ws_acta = wb.create_sheet(title="Acta de Cierre y Firmas")
    ws_acta.views.sheetView[0].showGridLines = True

    ws_acta.merge_cells("A1:E1")
    ws_acta["A1"] = (
        "ACTA FORMAL DE CORTE Y EMPALME CONTABLE - INGENIO VERDE INGEV S.A.S."
    )
    ws_acta["A1"].font = font_title
    ws_acta["A1"].fill = fill_navy
    ws_acta["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_acta.row_dimensions[1].height = 35

    texto_acta = (
        "En la ciudad de Yopal, Casanare, a los 27 días del mes de agosto de 2026, se reúnen los representantes de la firma "
        "TAX PAY S.A.S. (Contadores Salientes) y el profesional Jeffer Daniel Pacheco Peña (Contador Entrante), con el fin de realizar la "
        "entrega y recepción de la información contable, financiera y tributaria de la empresa INGENIO VERDE INGEV S.A.S.\n\n"
        "Se deja constancia de que los ítems marcados como 'RECIBIDO' han sido entregados a satisfacción, mientras que los ítems "
        "'PENDIENTES' o 'EN PROCESO' quedan con el compromiso de entrega formal en los plazos establecidos en las observaciones."
    )

    ws_acta.merge_cells("A3:E5")
    ws_acta["A3"] = texto_acta
    ws_acta["A3"].font = font_regular
    ws_acta["A3"].alignment = Alignment(wrap_text=True, vertical="top")

    # Firmas
    ws_acta["B9"] = "_____________________________________"
    ws_acta["B10"] = "ENTREGA (Firma Saliente)"
    ws_acta["B11"] = "TAX PAY S.A.S."
    ws_acta["B12"] = "NIT: 901.166.067-4"

    ws_acta["D9"] = "_____________________________________"
    ws_acta["D10"] = "RECIBE (Contador Entrante)"
    ws_acta["D11"] = "Jeffer Daniel Pacheco Peña"
    ws_acta["D12"] = "Contador Público"

    for r in range(9, 13):
        ws_acta[f"B{r}"].alignment = Alignment(horizontal="center")
        ws_acta[f"D{r}"].alignment = Alignment(horizontal="center")
        ws_acta[f"B{r}"].font = font_bold if r in (10, 11) else font_regular
        ws_acta[f"D{r}"].font = font_bold if r in (10, 11) else font_regular

    ws_acta.column_dimensions["A"].width = 5
    ws_acta.column_dimensions["B"].width = 35
    ws_acta.column_dimensions["C"].width = 10
    ws_acta.column_dimensions["D"].width = 35
    ws_acta.column_dimensions["E"].width = 5

    # Guardar Libro
    file_name = "Checklist_Empalme_INGEV_TAX_PAY.xlsx"
    wb.save(file_name)
    print(f"¡Archivo generado exitosamente como '{file_name}'!")


if __name__ == "__main__":
    crear_checklist_empalme()