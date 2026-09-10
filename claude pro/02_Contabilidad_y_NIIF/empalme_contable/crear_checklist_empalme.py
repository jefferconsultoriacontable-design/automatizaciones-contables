"""
Genera el checklist de empalme contable en Excel, listo para diligenciar y firmar.

    python crear_checklist_empalme.py --empresa "MI EMPRESA S.A.S." --entrega "Nombre saliente" --recibe "Nombre entrante"

Salida: un libro con cuatro hojas
    Checklist   - 70+ items por area, con responsable, estado, fecha y observaciones
    Resumen     - conteo por area y por estado (formulas vivas, se actualiza al diligenciar)
    Riesgos     - matriz de riesgos detectados en el empalme
    Acta        - modelo de acta de entrega y recibo para firmar

El objetivo del empalme no es recibir archivos: es dejar por escrito el estado real
de la contabilidad en la fecha de corte, para que las contingencias anteriores no
queden a nombre de quien recibe.
"""
from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

AZUL = "1F3B5C"
GRIS = "EEF1F5"

ITEMS: list[tuple[str, str, str]] = [
    # (area, item, criterio de aceptacion)
    ("1. Documentacion legal", "Certificado de existencia y representacion legal vigente", "No mayor a 30 dias"),
    ("1. Documentacion legal", "RUT actualizado con responsabilidades vigentes", "Verificar codigos de responsabilidad"),
    ("1. Documentacion legal", "Estatutos, actas de junta y de asamblea del ultimo ano", "Libro de actas al dia"),
    ("1. Documentacion legal", "Libros oficiales registrados y su estado de impresion", "Fecha del ultimo folio impreso"),
    ("1. Documentacion legal", "Poderes y facultades del representante legal", "Limites de contratacion"),
    ("1. Documentacion legal", "Contratos vigentes: arrendamientos, leasing, comodato, servicios", "Copia y fechas de vencimiento"),

    ("2. Estados financieros", "Estados financieros del ultimo cierre firmados", "Con notas y certificacion"),
    ("2. Estados financieros", "Balance de prueba a la fecha de corte del empalme", "A nivel de auxiliar"),
    ("2. Estados financieros", "Politicas contables bajo NIIF documentadas y aprobadas", "Grupo 1, 2 o 3 identificado"),
    ("2. Estados financieros", "Notas a los estados financieros del ultimo periodo", "Revelaciones completas"),
    ("2. Estados financieros", "Dictamen del revisor fiscal e informes de auditoria", "Salvedades y su seguimiento"),
    ("2. Estados financieros", "Ajustes de auditoria pendientes de registrar", "Listado con valor y cuenta"),

    ("3. Conciliaciones", "Conciliaciones bancarias de todas las cuentas a la fecha de corte", "Firmadas, con partidas conciliatorias explicadas"),
    ("3. Conciliaciones", "Partidas conciliatorias con antiguedad mayor a 90 dias", "Explicacion y plan de depuracion"),
    ("3. Conciliaciones", "Conciliacion de cartera contra el modulo o auxiliar de clientes", "Diferencia = 0"),
    ("3. Conciliaciones", "Conciliacion de proveedores contra estados de cuenta", "Circularizacion de los principales"),
    ("3. Conciliaciones", "Conciliacion de inventario contra toma fisica", "Fecha del ultimo conteo y diferencias"),
    ("3. Conciliaciones", "Conciliacion de nomina contra planilla PILA", "Por los ultimos 3 meses"),
    ("3. Conciliaciones", "Conciliacion de IVA e ICA contra declaraciones presentadas", "Cuentas 2408 y 2368"),
    ("3. Conciliaciones", "Conciliacion de retenciones contra declaraciones y certificados", "Cuenta 2365"),
    ("3. Conciliaciones", "Conciliacion de cuentas por cobrar y pagar a socios y vinculados", "Soportes de cada operacion"),

    ("4. Saldos y depuracion", "Cuentas puente y transitorias con saldo", "1330, 1355, 1380, 2335 y similares"),
    ("4. Saldos y depuracion", "Cuentas con saldo contrario a su naturaleza", "Listado y explicacion"),
    ("4. Saldos y depuracion", "Anticipos a proveedores y de clientes sin legalizar", "Antiguedad y soporte"),
    ("4. Saldos y depuracion", "Cartera con antiguedad mayor a 360 dias", "Estado de la gestion de cobro"),
    ("4. Saldos y depuracion", "Deterioro de cartera calculado y reconocido (NIIF 9)", "Metodologia documentada"),
    ("4. Saldos y depuracion", "Inventario obsoleto o de lenta rotacion", "Ajuste a valor neto realizable"),
    ("4. Saldos y depuracion", "Diferencias entre el modulo de activos fijos y la contabilidad", "Conciliacion firmada"),

    ("5. Tributaria", "Declaraciones de renta de los ultimos 3 anos con soporte de pago", "Firmes o dentro del termino"),
    ("5. Tributaria", "Declaraciones de IVA del ultimo ano", "Todas presentadas y pagadas"),
    ("5. Tributaria", "Declaraciones de retencion en la fuente del ultimo ano", "Sin ineficacia por falta de pago"),
    ("5. Tributaria", "Declaraciones de ICA municipales", "Por cada municipio donde hay actividad"),
    ("5. Tributaria", "Informacion exogena nacional y municipal presentada", "Acuse de recibo DIAN"),
    ("5. Tributaria", "Requerimientos, emplazamientos o pliegos de cargos en curso", "Fechas de respuesta"),
    ("5. Tributaria", "Saldos a favor y su estado (imputacion o devolucion)", "Valor y vigencia"),
    ("5. Tributaria", "Correcciones presentadas y sanciones liquidadas", "Historial de los 3 ultimos anos"),
    ("5. Tributaria", "Facturacion electronica: resoluciones, rangos y estado del proveedor", "Vigencia de la numeracion"),
    ("5. Tributaria", "Documento soporte en adquisiciones con no obligados a facturar", "Cumplimiento del requisito"),
    ("5. Tributaria", "Calendario tributario del ano con responsables", "Por ultimo digito del NIT"),

    ("6. Nomina y laboral", "Contratos laborales vigentes y su modalidad", "Archivo completo por empleado"),
    ("6. Nomina y laboral", "Liquidacion de prestaciones sociales consolidadas", "Cesantias, intereses, prima, vacaciones"),
    ("6. Nomina y laboral", "Pagos de seguridad social al dia (PILA)", "Ultimos 12 meses"),
    ("6. Nomina y laboral", "Nomina electronica transmitida a la DIAN", "Sin documentos rechazados"),
    ("6. Nomina y laboral", "Procesos laborales en curso y provisiones asociadas", "Concepto del abogado"),
    ("6. Nomina y laboral", "Dotacion, examenes medicos y SG-SST", "Estado de cumplimiento"),

    ("7. Tesoreria y activos", "Inventario de cuentas bancarias, firmas y tokens", "Autorizados vigentes"),
    ("7. Tesoreria y activos", "Obligaciones financieras: saldos, tasas y garantias", "Extractos y plan de pagos"),
    ("7. Tesoreria y activos", "Arqueo de caja y de caja menor a la fecha de corte", "Acta firmada"),
    ("7. Tesoreria y activos", "Inventario fisico de propiedad, planta y equipo", "Con placa, ubicacion y responsable"),
    ("7. Tesoreria y activos", "Polizas de seguro vigentes", "Coberturas y vencimientos"),
    ("7. Tesoreria y activos", "Cheques girados y no cobrados", "Listado con antiguedad"),

    ("8. Sistemas y accesos", "Usuario y perfil en el software contable", "Con permisos de cierre y reportes"),
    ("8. Sistemas y accesos", "Copias de seguridad: ubicacion, periodicidad y prueba de restauracion", "Evidencia de la ultima prueba"),
    ("8. Sistemas y accesos", "Accesos a portales DIAN, municipio, bancos y operadores", "Firma electronica y su vigencia"),
    ("8. Sistemas y accesos", "Periodos contables cerrados o bloqueados en el sistema", "Fecha del ultimo cierre"),
    ("8. Sistemas y accesos", "Plan unico de cuentas parametrizado y sus cuentas inactivas", "Documentado"),
    ("8. Sistemas y accesos", "Parametrizacion de impuestos y retenciones en el sistema", "Tarifas y bases vigentes"),

    ("9. Procesos y control", "Manual de procedimientos contables y flujos de aprobacion", "Actualizado"),
    ("9. Procesos y control", "Calendario de cierre mensual con responsables", "Dias y entregables"),
    ("9. Procesos y control", "Informes recurrentes a gerencia, junta y entes de control", "Formato y fechas"),
    ("9. Procesos y control", "Terceros clave: revisor fiscal, asesores, proveedor del software", "Contactos y contratos"),
    ("9. Procesos y control", "Obligaciones ante Supersociedades u otros supervisores", "Estado y vencimientos"),
    ("9. Procesos y control", "Reportes de SARLAFT / SAGRLAFT si aplica", "Oficial de cumplimiento designado"),

    ("10. Cierre del empalme", "Acta de entrega y recibo firmada por ambas partes", "Con fecha de corte explicita"),
    ("10. Cierre del empalme", "Inventario documental entregado (fisico y digital)", "Relacion detallada"),
    ("10. Cierre del empalme", "Salvedades y contingencias declaradas por escrito", "Firmadas por quien entrega"),
    ("10. Cierre del empalme", "Plan de trabajo de los primeros 30 dias de quien recibe", "Priorizado por riesgo"),
]

RIESGOS = [
    ("Declaraciones de retencion presentadas sin pago", "Ineficacia de la declaracion (Art. 580-1 ET)", "ALTO"),
    ("Cartera antigua sin deterioro", "Sobreestimacion del activo y de la utilidad", "ALTO"),
    ("Partidas conciliatorias antiguas sin depurar", "Saldo de bancos no representa la realidad", "ALTO"),
    ("Prestaciones sociales sin consolidar", "Subestimacion del pasivo laboral", "ALTO"),
    ("Exogena presentada con inconsistencias", "Sancion por informacion errónea (Art. 651 ET)", "MEDIO"),
    ("Inventario sin toma fisica reciente", "Diferencias no identificadas en el costo de ventas", "MEDIO"),
    ("Activos fijos sin conciliar con el modulo", "Depreciacion mal calculada", "MEDIO"),
    ("Sin copia de seguridad probada", "Perdida de informacion contable", "MEDIO"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--empresa", default="LA COMPANIA S.A.S.")
    ap.add_argument("--nit", default="900.000.000-0")
    ap.add_argument("--entrega", default="(contador saliente)")
    ap.add_argument("--recibe", default="(contador entrante)")
    ap.add_argument("--corte", default=date.today().strftime("%d/%m/%Y"))
    ap.add_argument("--salida", default="salidas/checklist_empalme.xlsx")
    args = ap.parse_args()

    wb = Workbook()
    borde = Border(*[Side(style="thin", color="C9D2DC")] * 4)
    th = Font(bold=True, color="FFFFFF", size=10)
    fill_h = PatternFill("solid", fgColor=AZUL)

    # ---------------------------------------------------------- Checklist
    ws = wb.active
    ws.title = "Checklist"
    ws["A1"] = f"CHECKLIST DE EMPALME CONTABLE - {args.empresa} (NIT {args.nit})"
    ws["A1"].font = Font(bold=True, size=13, color=AZUL)
    ws["A2"] = (f"Fecha de corte: {args.corte}   |   Entrega: {args.entrega}   |   "
                f"Recibe: {args.recibe}")
    ws["A2"].font = Font(size=9.5, color="555F6D")

    encabezados = ["#", "Area", "Item a verificar", "Criterio de aceptacion",
                   "Estado", "Responsable", "Fecha", "Observaciones"]
    ws.append([])
    ws.append(encabezados)
    for c in ws[4]:
        c.font, c.fill, c.border = th, fill_h, borde
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for i, (area, item, criterio) in enumerate(ITEMS, 1):
        ws.append([i, area, item, criterio, "PENDIENTE", "", "", ""])
    fin = ws.max_row

    dv = DataValidation(type="list",
                        formula1='"PENDIENTE,RECIBIDO,CON SALVEDAD,NO APLICA"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(f"E5:E{fin}")

    for fila in ws.iter_rows(min_row=5, max_row=fin, max_col=8):
        for c in fila:
            c.border = borde
            c.alignment = Alignment(vertical="top", wrap_text=True)
        if fila[0].row % 2 == 1:
            for c in fila:
                c.fill = PatternFill("solid", fgColor=GRIS)

    for col, ancho in zip("ABCDEFGH", [5, 24, 52, 38, 16, 20, 12, 34]):
        ws.column_dimensions[col].width = ancho
    ws.freeze_panes = "A5"
    ws.auto_filter.ref = f"A4:H{fin}"

    # ------------------------------------------------------------ Resumen
    r = wb.create_sheet("Resumen")
    r["A1"] = "RESUMEN DEL EMPALME"
    r["A1"].font = Font(bold=True, size=13, color=AZUL)
    r.append([])
    r.append(["Estado", "Cantidad", "% del total"])
    for c in r[3]:
        c.font, c.fill, c.border = th, fill_h, borde
    for i, estado in enumerate(["PENDIENTE", "RECIBIDO", "CON SALVEDAD", "NO APLICA"], start=4):
        r[f"A{i}"] = estado
        r[f"B{i}"] = f'=COUNTIF(Checklist!$E$5:$E${fin},A{i})'
        r[f"C{i}"] = f'=IF($B$8=0,0,B{i}/{len(ITEMS)})'
        r[f"C{i}"].number_format = "0.0%"
    r["A8"] = "TOTAL"
    r["A8"].font = Font(bold=True)
    r["B8"] = f"=SUM(B4:B7)"
    r["B8"].font = Font(bold=True)

    r["A10"] = "Avance por area"
    r["A10"].font = Font(bold=True, size=11, color=AZUL)
    r.append([])
    r["A11"], r["B11"], r["C11"] = "Area", "Items", "Recibidos"
    for c in r[11]:
        c.font, c.fill, c.border = th, fill_h, borde
    areas = sorted({a for a, _, _ in ITEMS})
    for i, area in enumerate(areas, start=12):
        r[f"A{i}"] = area
        r[f"B{i}"] = f'=COUNTIF(Checklist!$B$5:$B${fin},A{i})'
        r[f"C{i}"] = f'=COUNTIFS(Checklist!$B$5:$B${fin},A{i},Checklist!$E$5:$E${fin},"RECIBIDO")'
    for col, ancho in zip("ABC", [28, 12, 14]):
        r.column_dimensions[col].width = ancho

    # ------------------------------------------------------------ Riesgos
    rg = wb.create_sheet("Riesgos")
    rg["A1"] = "MATRIZ DE RIESGOS DEL EMPALME"
    rg["A1"].font = Font(bold=True, size=13, color=AZUL)
    rg.append([])
    rg.append(["Riesgo detectado", "Consecuencia", "Nivel", "Aplica (SI/NO)", "Plan de accion", "Responsable", "Fecha limite"])
    for c in rg[3]:
        c.font, c.fill, c.border = th, fill_h, borde
    for riesgo, consecuencia, nivel in RIESGOS:
        rg.append([riesgo, consecuencia, nivel, "", "", "", ""])
    for fila in rg.iter_rows(min_row=4, max_row=rg.max_row, max_col=7):
        for c in fila:
            c.border = borde
            c.alignment = Alignment(vertical="top", wrap_text=True)
    for col, ancho in zip("ABCDEFG", [42, 42, 10, 14, 40, 20, 14]):
        rg.column_dimensions[col].width = ancho

    # -------------------------------------------------------------- Acta
    ac = wb.create_sheet("Acta")
    texto = [
        f"ACTA DE ENTREGA Y RECIBO DEL AREA CONTABLE",
        "",
        f"Empresa: {args.empresa}   NIT: {args.nit}",
        f"Fecha de corte de la entrega: {args.corte}",
        f"Entrega: {args.entrega}",
        f"Recibe: {args.recibe}",
        "",
        "1. OBJETO. Dejar constancia del estado de la informacion contable, financiera y",
        "   tributaria de la compania a la fecha de corte senalada, asi como de los documentos",
        "   y accesos entregados a quien recibe.",
        "",
        "2. ALCANCE. Quien recibe asume la responsabilidad profesional sobre los hechos",
        "   economicos ocurridos a partir de la fecha de corte. Los periodos anteriores quedan",
        "   bajo la responsabilidad de quien entrega, salvo lo expresamente aceptado en esta acta.",
        "",
        "3. DOCUMENTOS ENTREGADOS. Se relacionan en la hoja Checklist de este mismo archivo,",
        "   con su estado individual (RECIBIDO, CON SALVEDAD, PENDIENTE o NO APLICA).",
        "",
        "4. SALVEDADES Y CONTINGENCIAS DECLARADAS:",
        "   ______________________________________________________________________________",
        "   ______________________________________________________________________________",
        "   ______________________________________________________________________________",
        "",
        "5. PENDIENTES CON PLAZO ACORDADO:",
        "   ______________________________________________________________________________",
        "   ______________________________________________________________________________",
        "",
        "En constancia se firma en ____________________ el ____ de __________ de 20____.",
        "",
        "",
        "___________________________________        ___________________________________",
        f"{args.entrega}".ljust(42) + f"{args.recibe}",
        "C.C.                                       C.C.",
        "T.P.                                       T.P.",
        "Entrega                                    Recibe",
    ]
    for i, linea in enumerate(texto, start=1):
        ac[f"A{i}"] = linea
        if i == 1:
            ac[f"A{i}"].font = Font(bold=True, size=13, color=AZUL)
    ac.column_dimensions["A"].width = 100

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    wb.save(salida)
    print(f"Checklist generado: {salida}")
    print(f"Items: {len(ITEMS)} en {len(areas)} areas | Riesgos precargados: {len(RIESGOS)}")


if __name__ == "__main__":
    main()
