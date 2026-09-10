"""Genera los datasets contables simulados del curso de pandas.
Empresa ficticia: COMERCIALIZADORA ANDINA S.A.S. - NIT 900.111.222-3
Periodo: 01-01-2026 a 31-03-2026
"""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(2026)
OUT = "datos"

import os
os.makedirs(OUT, exist_ok=True)

PUC = {
    "110505": ("Caja general", "D"),
    "111005": ("Banco Bogota cta corriente 123-456", "D"),
    "130505": ("Clientes nacionales", "D"),
    "135515": ("Retencion en la fuente a favor", "D"),
    "135517": ("Retencion de ICA a favor", "D"),
    "143530": ("Mercancias no fabricadas por la empresa", "D"),
    "152405": ("Equipo de oficina", "D"),
    "159210": ("Depreciacion acumulada equipo de oficina", "C"),
    "220505": ("Proveedores nacionales", "C"),
    "233595": ("Costos y gastos por pagar", "C"),
    "236540": ("Retencion en la fuente por pagar", "C"),
    "236805": ("Impuesto de industria y comercio retenido", "C"),
    "237005": ("Aportes a entidades de seguridad social", "C"),
    "240805": ("IVA generado", "C"),
    "240810": ("IVA descontable", "D"),
    "250505": ("Salarios por pagar", "C"),
    "310505": ("Capital suscrito y pagado", "C"),
    "360505": ("Utilidad del ejercicio", "C"),
    "370505": ("Utilidades acumuladas", "C"),
    "413595": ("Comercio al por mayor y menor", "C"),
    "421005": ("Rendimientos financieros", "C"),
    "613595": ("Costo de venta de mercancias", "D"),
    "510506": ("Sueldos", "D"),
    "510568": ("Aportes ARL, salud y pension", "D"),
    "513525": ("Servicios de energia", "D"),
    "513530": ("Servicios de telefono e internet", "D"),
    "513595": ("Otros servicios", "D"),
    "516010": ("Depreciacion equipo de oficina", "D"),
    "530525": ("Gastos bancarios", "D"),
    "531520": ("Gravamen a los movimientos financieros", "D"),
}

TERCEROS_CLI = [
    ("901234567", "SUPERMERCADOS DEL LLANO S.A.S."),
    ("800112233", "DISTRIBUIDORA EL PORTAL LTDA"),
    ("901998877", "TIENDAS LA ESQUINA S.A.S."),
    ("830445566", "MAYORISTA CASANARE S.A.S."),
    ("901556677", "COMERCIAL YOPAL SAS"),
]
TERCEROS_PRO = [
    ("890900608", "ALIMENTOS NACIONALES S.A."),
    ("860002964", "EMPAQUES Y PLASTICOS LTDA"),
    ("900321654", "LOGISTICA ANDINA S.A.S."),
    ("811004321", "PAPELERIA CENTRAL SAS"),
    ("900777888", "SERVICIOS INTEGRALES DEL ORIENTE SAS"),
]
CENTROS = ["ADM", "VTA", "OPE"]

rows = []          # libro auxiliar
facturas = []      # facturas de proveedores
consec = {"FV": 0, "FC": 0, "RC": 0, "CE": 0, "NOM": 0, "DP": 0}


def add(f, comp, cta, nit, nombre, detalle, deb, cre, cc):
    rows.append({
        "fecha": f,
        "comprobante": comp,
        "codigo_puc": cta,
        "nombre_cuenta": PUC[cta][0],
        "nit_tercero": nit,
        "nombre_tercero": nombre,
        "detalle": detalle,
        "debito": round(deb, 2),
        "credito": round(cre, 2),
        "centro_costo": cc,
    })


def doc(tipo):
    consec[tipo] += 1
    return f"{tipo}-{consec[tipo]:04d}"


ini = date(2026, 1, 1)
dias = [ini + timedelta(days=i) for i in range((date(2026, 3, 31) - ini).days + 1)]
habiles = [d for d in dias if d.weekday() < 5]

# ---------------- VENTAS ----------------
for d in habiles:
    for _ in range(random.randint(1, 3)):
        nit, cli = random.choice(TERCEROS_CLI)
        base = round(random.randint(800, 9000) * 1000, 2)
        iva = round(base * 0.19, 2)
        retiene = base >= 3000000
        rf = round(base * 0.025, 2) if retiene else 0.0
        ica = round(base * 0.00966, 2) if retiene else 0.0
        cxc = round(base + iva - rf - ica, 2)
        c = doc("FV")
        add(d, c, "130505", nit, cli, "Venta de mercancia", cxc, 0, "VTA")
        if retiene:
            add(d, c, "135515", nit, cli, "Retefuente que nos practican", rf, 0, "VTA")
            add(d, c, "135517", nit, cli, "ReteICA que nos practican", ica, 0, "VTA")
        add(d, c, "413595", nit, cli, "Venta de mercancia", 0, base, "VTA")
        add(d, c, "240805", nit, cli, "IVA generado 19%", 0, iva, "VTA")
        costo = round(base * random.uniform(0.58, 0.68), 2)
        add(d, c, "613595", nit, cli, "Costo de la venta", costo, 0, "VTA")
        add(d, c, "143530", nit, cli, "Salida de inventario", 0, costo, "VTA")

# ---------------- COMPRAS ----------------
for d in habiles:
    if random.random() < 0.55:
        nit, prov = random.choice(TERCEROS_PRO)
        base = round(random.randint(500, 7000) * 1000, 2)
        iva = round(base * 0.19, 2)
        rf = round(base * 0.025, 2)
        ica = round(base * 0.00966, 2)
        neto = round(base + iva - rf - ica, 2)
        c = doc("FC")
        num_fact = f"FE{random.randint(10000, 99999)}"
        add(d, c, "143530", nit, prov, f"Compra mercancia {num_fact}", base, 0, "OPE")
        add(d, c, "240810", nit, prov, "IVA descontable 19%", iva, 0, "OPE")
        add(d, c, "236540", nit, prov, "Retefuente compras 2.5%", 0, rf, "OPE")
        add(d, c, "236805", nit, prov, "ReteICA 9.66x1000", 0, ica, "OPE")
        add(d, c, "220505", nit, prov, f"Factura {num_fact}", 0, neto, "OPE")
        facturas.append({
            "numero_factura": num_fact,
            "fecha_factura": d.strftime("%d/%m/%Y"),
            "nit_proveedor": nit,
            "proveedor": prov,
            "concepto": "Compra de mercancia",
            "base_gravable": base,
            "iva": iva,
            "retefuente": rf,
            "reteica": ica,
            "neto_a_pagar": neto,
            "estado": random.choice(["PAGADA", "PENDIENTE", "PENDIENTE"]),
        })

# ---------------- RECAUDOS ----------------
for d in habiles:
    for _ in range(random.randint(0, 2)):
        nit, cli = random.choice(TERCEROS_CLI)
        v = round(random.randint(1000, 9000) * 1000, 2)
        c = doc("RC")
        add(d, c, "111005", nit, cli, "Recaudo cliente", v, 0, "ADM")
        add(d, c, "130505", nit, cli, "Abono cartera", 0, v, "ADM")
        gmf = round(v * 0.004, 2)

# ---------------- PAGOS A PROVEEDORES ----------------
for d in habiles:
    if random.random() < 0.45:
        nit, prov = random.choice(TERCEROS_PRO)
        v = round(random.randint(800, 7000) * 1000, 2)
        c = doc("CE")
        add(d, c, "220505", nit, prov, "Pago factura proveedor", v, 0, "ADM")
        add(d, c, "111005", nit, prov, "Pago factura proveedor", 0, v, "ADM")

# ---------------- SERVICIOS ----------------
servicios = [("513525", "Energia"), ("513530", "Internet y telefonia"), ("513595", "Aseo y vigilancia")]
for mes in (1, 2, 3):
    for cta, nom in servicios:
        d = date(2026, mes, 20)
        v = round(random.randint(300, 1200) * 1000, 2)
        c = doc("CE")
        add(d, c, cta, "900777888", "SERVICIOS INTEGRALES DEL ORIENTE SAS", nom, v, 0, "ADM")
        add(d, c, "111005", "900777888", "SERVICIOS INTEGRALES DEL ORIENTE SAS", nom, 0, v, "ADM")

# ---------------- NOMINA ----------------
for mes in (1, 2, 3):
    d = date(2026, mes, 28)
    sueldos = 24_800_000.0
    aportes = round(sueldos * 0.205, 2)
    c = doc("NOM")
    add(d, c, "510506", "900111222", "NOMINA", f"Nomina mes {mes:02d}", sueldos, 0, "ADM")
    add(d, c, "510568", "900111222", "NOMINA", f"Aportes mes {mes:02d}", aportes, 0, "ADM")
    add(d, c, "250505", "900111222", "NOMINA", f"Salarios por pagar mes {mes:02d}", 0, sueldos, "ADM")
    add(d, c, "237005", "900111222", "NOMINA", f"Seguridad social mes {mes:02d}", 0, aportes, "ADM")

# ---------------- DEPRECIACION ----------------
for mes in (1, 2, 3):
    d = date(2026, mes, 28) if mes != 2 else date(2026, 2, 27)
    v = 1_250_000.0
    c = doc("DP")
    add(d, c, "516010", "900111222", "COMERCIALIZADORA ANDINA SAS", "Depreciacion mensual", v, 0, "ADM")
    add(d, c, "159210", "900111222", "COMERCIALIZADORA ANDINA SAS", "Depreciacion mensual", 0, v, "ADM")

aux = pd.DataFrame(rows).sort_values(["fecha", "comprobante"]).reset_index(drop=True)
assert round(aux.debito.sum() - aux.credito.sum(), 2) == 0, "El auxiliar no cuadra"

# ---------------- SALDOS INICIALES ----------------
saldos_ini = {
    "110505": 3_500_000.0,
    "111005": 185_000_000.0,
    "130505": 96_400_000.0,
    "143530": 210_000_000.0,
    "152405": 75_000_000.0,
    "159210": -18_750_000.0,
    "220505": -84_150_000.0,
    "310505": -300_000_000.0,
    "370505": -167_000_000.0,
}
assert round(sum(saldos_ini.values()), 2) == 0, "Los saldos iniciales no cuadran"

mov = aux.groupby("codigo_puc")[["debito", "credito"]].sum()
bp = []
for cta, (nombre, nat) in PUC.items():
    si = saldos_ini.get(cta, 0.0)
    si = abs(si) if cta in saldos_ini else 0.0
    if cta in saldos_ini and saldos_ini[cta] < 0:
        si_deb, si_cre = 0.0, abs(saldos_ini[cta])
    else:
        si_deb, si_cre = si, 0.0
    deb = float(mov.debito.get(cta, 0.0))
    cre = float(mov.credito.get(cta, 0.0))
    neto = (si_deb - si_cre) + deb - cre
    bp.append({
        "codigo_puc": cta,
        "nombre_cuenta": nombre,
        "naturaleza": nat,
        "saldo_inicial": round(si_deb - si_cre, 2),
        "debitos": round(deb, 2),
        "creditos": round(cre, 2),
        "saldo_final": round(neto, 2),
    })
bp = pd.DataFrame(bp)
assert round(bp.saldo_final.sum(), 2) == 0, "El balance de prueba no cuadra"

# ---------------- EXTRACTO BANCARIO ----------------
banco = aux[aux.codigo_puc == "111005"].copy()
banco["valor_libros"] = banco.debito - banco.credito
ext = []
saldo = 185_000_000.0
pendientes_libros = []
for i, r in banco.sort_values("fecha").iterrows():
    if random.random() < 0.06:            # cheque / consignacion pendiente: no llega al banco
        pendientes_libros.append(r)
        continue
    f = r.fecha
    if random.random() < 0.08:            # partida en transito: llega 2 dias despues
        f = f + timedelta(days=2)
    ext.append({
        "fecha": f,
        "descripcion": ("CONSIGNACION " if r.valor_libros > 0 else "PAGO ") + str(r.nombre_tercero)[:28],
        "referencia": r.comprobante,
        "valor": round(float(r.valor_libros), 2),
    })
    if r.valor_libros < 0:                # GMF 4x1000 sobre los debitos del banco
        ext.append({
            "fecha": f,
            "descripcion": "GMF 4X1000",
            "referencia": "GMF",
            "valor": round(float(r.valor_libros) * 0.004, 2),
        })
for mes in (1, 2, 3):
    ext.append({"fecha": date(2026, mes, 28), "descripcion": "COMISION MANEJO CUENTA",
                "referencia": "COM", "valor": -35000.0})
    ext.append({"fecha": date(2026, mes, 28), "descripcion": "RENDIMIENTOS FINANCIEROS",
                "referencia": "REND", "valor": round(random.randint(90, 260) * 1000.0, 2)})
ext.append({"fecha": date(2026, 2, 17), "descripcion": "NOTA DEBITO CHEQUE DEVUELTO",
            "referencia": "ND-0001", "valor": -4_800_000.0})
ext = pd.DataFrame(ext).sort_values(["fecha", "referencia"]).reset_index(drop=True)
ext["saldo"] = (saldo + ext.valor.cumsum()).round(2)

# ---------------- FACTURAS: se ensucia a proposito ----------------
fac = pd.DataFrame(facturas)
fac.loc[fac.sample(frac=0.12, random_state=7).index, "proveedor"] = \
    fac.loc[fac.sample(frac=0.12, random_state=7).index, "proveedor"].str.lower()
idx = fac.sample(frac=0.08, random_state=3).index
fac.loc[idx, "proveedor"] = "  " + fac.loc[idx, "proveedor"] + "  "
fac.loc[fac.sample(frac=0.05, random_state=11).index, "estado"] = None
fac = pd.concat([fac, fac.sample(4, random_state=5)], ignore_index=True)   # duplicados
fac = fac.sample(frac=1, random_state=13).reset_index(drop=True)

aux.to_csv(f"{OUT}/libro_auxiliar.csv", index=False, encoding="utf-8")
bp.to_csv(f"{OUT}/balance_prueba.csv", index=False, encoding="utf-8")
ext.to_csv(f"{OUT}/extracto_bancario.csv", index=False, encoding="utf-8")
fac.to_csv(f"{OUT}/facturas_proveedores.csv", index=False, encoding="utf-8")

print("libro_auxiliar   :", aux.shape, "| debitos == creditos:", round(aux.debito.sum(), 2) == round(aux.credito.sum(), 2))
print("balance_prueba   :", bp.shape, "| suma saldos finales:", round(bp.saldo_final.sum(), 2))
print("extracto_bancario:", ext.shape)
print("facturas         :", fac.shape, "| duplicados:", int(fac.duplicated().sum()))
print("saldo libros 1110:", round(bp.loc[bp.codigo_puc == '111005', 'saldo_final'].iloc[0], 2))
print("saldo extracto   :", round(ext.saldo.iloc[-1], 2))
