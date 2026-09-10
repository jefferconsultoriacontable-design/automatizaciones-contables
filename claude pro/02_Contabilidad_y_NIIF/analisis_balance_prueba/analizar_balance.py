"""
Analizador de balance de prueba con enfoque de auditoria y NIIF.

    python analizar_balance.py balance_prueba.csv
    python analizar_balance.py balance.xlsx --salida salidas/analisis_marzo.xlsx

Que revisa
----------
1. VALIDACIONES ARITMETICAS
   - suma de debitos = suma de creditos
   - saldo final = saldo inicial + debitos - creditos, cuenta por cuenta
   - ecuacion contable: Activo = Pasivo + Patrimonio + Resultado del ejercicio

2. INDICADORES FINANCIEROS
   razon corriente, prueba acida, capital de trabajo, endeudamiento,
   margen bruto, margen operacional, rotacion de cartera e inventarios

3. ALERTAS TECNICAS (revisiones que un revisor fiscal pregunta primero)
   - cuentas con saldo contrario a su naturaleza
   - cartera sin deterioro reconocido (NIIF 9 / Seccion 11 - perdida esperada)
   - inventario sin ajuste a valor neto realizable (NIC 2 / Seccion 13)
   - propiedad planta y equipo sin depreciacion del periodo (NIC 16 / Seccion 17)
   - anticipos y partidas puente sin depurar
   - ausencia de impuesto diferido (NIC 12 / Seccion 29)
   - ausencia de provisiones y beneficios a empleados (NIC 37 y NIC 19)

Convencion de signos: los saldos credito llegan en negativo en 'saldo_final'.
Si tu archivo trae los saldos en positivo con una columna 'naturaleza' (D/C),
el script los convierte automaticamente.
"""
from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import pandas as pd

ALIAS = {
    "cuenta": "codigo_puc", "codigo": "codigo_puc", "codigo_cuenta": "codigo_puc", "puc": "codigo_puc",
    "nombre": "nombre_cuenta", "descripcion": "nombre_cuenta", "cuenta_nombre": "nombre_cuenta",
    "saldo_anterior": "saldo_inicial", "saldo_inicial_": "saldo_inicial",
    "debe": "debitos", "haber": "creditos", "debito": "debitos", "credito": "creditos",
    "movimiento_debito": "debitos", "movimiento_credito": "creditos",
    "saldo": "saldo_final", "saldo_actual": "saldo_final", "nuevo_saldo": "saldo_final",
}
CLASES = {"1": "ACTIVO", "2": "PASIVO", "3": "PATRIMONIO",
          "4": "INGRESOS", "5": "GASTOS", "6": "COSTOS", "7": "COSTOS DE PRODUCCION"}
NATURALEZA_CLASE = {"1": "D", "2": "C", "3": "C", "4": "C", "5": "D", "6": "D", "7": "D"}


def norm(c: str) -> str:
    s = unicodedata.normalize("NFKD", str(c)).encode("ascii", "ignore").decode()
    s = s.strip().lower().replace(" ", "_")
    return ALIAS.get(s, s)


def cargar(ruta: Path) -> pd.DataFrame:
    df = (pd.read_excel(ruta, dtype={"codigo_puc": str}) if ruta.suffix.lower().startswith(".xls")
          else pd.read_csv(ruta, dtype={"codigo_puc": str}, sep=None, engine="python"))
    df.columns = [norm(c) for c in df.columns]
    if "codigo_puc" not in df.columns:
        raise SystemExit("El archivo debe traer una columna de codigo de cuenta (codigo_puc).")
    df["codigo_puc"] = df["codigo_puc"].astype(str).str.strip()
    for c in ("saldo_inicial", "debitos", "creditos", "saldo_final"):
        df[c] = pd.to_numeric(df.get(c), errors="coerce").fillna(0.0)
    if "nombre_cuenta" not in df.columns:
        df["nombre_cuenta"] = ""

    # si vienen todos positivos con columna naturaleza, se ajusta el signo
    if "naturaleza" in df.columns and (df["saldo_final"] >= 0).all():
        signo = df["naturaleza"].astype(str).str.upper().str[0].map({"D": 1, "C": -1}).fillna(1)
        if abs((df["saldo_final"] * signo).sum()) < abs(df["saldo_final"].sum()):
            df["saldo_final"] = df["saldo_final"] * signo
            df["saldo_inicial"] = df["saldo_inicial"] * signo

    df["clase"] = df["codigo_puc"].str[0]
    df["clase_nombre"] = df["clase"].map(CLASES).fillna("SIN CLASIFICAR")
    df["grupo"] = df["codigo_puc"].str[:2]
    return df


def saldo(df: pd.DataFrame, *prefijos: str) -> float:
    m = df["codigo_puc"].str.startswith(prefijos)
    return round(float(df.loc[m, "saldo_final"].sum()), 2)


def validaciones(df: pd.DataFrame) -> pd.DataFrame:
    v = []
    dif_pd = round(df["debitos"].sum() - df["creditos"].sum(), 2)
    v.append(("Partida doble (debitos = creditos)", dif_pd, "OK" if dif_pd == 0 else "DESCUADRE"))

    if df[["saldo_inicial", "debitos", "creditos"]].abs().sum().sum() > 0:
        calc = df["saldo_inicial"] + df["debitos"] - df["creditos"]
        malas = int(((calc - df["saldo_final"]).abs().round(2) > 0.01).sum())
        v.append(("Cuentas donde saldo final <> inicial + debitos - creditos",
                  malas, "OK" if malas == 0 else "REVISAR"))

    activo = saldo(df, "1")
    pasivo = -saldo(df, "2")
    patrimonio = -saldo(df, "3")
    resultado = -(saldo(df, "4") + saldo(df, "5") + saldo(df, "6") + saldo(df, "7"))
    dif_ec = round(activo - (pasivo + patrimonio + resultado), 2)
    v += [
        ("Activo", activo, ""),
        ("Pasivo", pasivo, ""),
        ("Patrimonio", patrimonio, ""),
        ("Resultado del ejercicio", resultado, ""),
        ("Ecuacion contable (Activo - Pasivo - Patrimonio - Resultado)",
         dif_ec, "OK" if dif_ec == 0 else "DESCUADRE"),
    ]
    return pd.DataFrame(v, columns=["validacion", "valor", "estado"])


def indicadores(df: pd.DataFrame) -> pd.DataFrame:
    # convencion: corriente = grupos 11 a 14 en activo; 21 a 25 en pasivo
    act_cte = saldo(df, "11", "12", "13", "14")
    inventarios = saldo(df, "14")
    activo_total = saldo(df, "1")
    pas_cte = -saldo(df, "21", "22", "23", "24", "25")
    pasivo_total = -saldo(df, "2")
    patrimonio = -saldo(df, "3")
    ingresos = -saldo(df, "41")
    otros_ing = -saldo(df, "42")
    costos = saldo(df, "6", "7")
    gastos = saldo(df, "5")
    cartera = saldo(df, "13")

    ub = ingresos - costos
    uo = ub - gastos

    def div(a, b):
        return round(a / b, 2) if b else None

    filas = [
        ("Razon corriente", div(act_cte, pas_cte), "veces", "> 1,5 comodo"),
        ("Prueba acida", div(act_cte - inventarios, pas_cte), "veces", "> 1,0 comodo"),
        ("Capital de trabajo", round(act_cte - pas_cte, 2), "$", "positivo"),
        ("Nivel de endeudamiento", div(pasivo_total * 100, activo_total), "%", "< 60%"),
        ("Apalancamiento (pasivo/patrimonio)", div(pasivo_total, patrimonio), "veces", "< 1,5"),
        ("Margen bruto", div(ub * 100, ingresos), "%", "segun el sector"),
        ("Margen operacional", div(uo * 100, ingresos), "%", "segun el sector"),
        ("Rotacion de cartera", div(ingresos, cartera), "veces", "mayor es mejor"),
        ("Dias de cartera", div(cartera * 360, ingresos), "dias", "vs. politica de credito"),
        ("Rotacion de inventarios", div(costos, inventarios), "veces", "mayor es mejor"),
        ("Dias de inventario", div(inventarios * 360, costos), "dias", "vs. politica de compras"),
        ("Ingresos operacionales", round(ingresos, 2), "$", ""),
        ("Otros ingresos", round(otros_ing, 2), "$", ""),
        ("Utilidad bruta", round(ub, 2), "$", ""),
        ("Utilidad operacional", round(uo, 2), "$", ""),
    ]
    return pd.DataFrame(filas, columns=["indicador", "valor", "unidad", "referencia"])


def alertas(df: pd.DataFrame) -> pd.DataFrame:
    A = []

    def add(nivel, norma, hallazgo, accion):
        A.append({"nivel": nivel, "norma": norma, "hallazgo": hallazgo, "accion_sugerida": accion})

    # 1. saldos contrarios a la naturaleza
    con_saldo = df[df["saldo_final"] != 0].copy()
    con_saldo["nat"] = con_saldo["clase"].map(NATURALEZA_CLASE)
    contrarias = con_saldo[
        ((con_saldo["nat"] == "D") & (con_saldo["saldo_final"] < 0))
        | ((con_saldo["nat"] == "C") & (con_saldo["saldo_final"] > 0))
    ]
    # cuentas que por diseno tienen saldo contrario a su clase (correctoras y de IVA)
    EXCEPCIONES = ("1592", "1596", "1399", "1499", "2408", "1355", "1360", "1365")
    contrarias = contrarias[~contrarias["codigo_puc"].str.startswith(EXCEPCIONES)]
    for _, r in contrarias.iterrows():
        add("ALTA", "Marco conceptual - reconocimiento",
            f"Cuenta {r['codigo_puc']} {r['nombre_cuenta']} con saldo contrario a su naturaleza "
            f"({r['saldo_final']:,.2f})",
            "Identificar el origen: puede ser una reclasificacion pendiente o un registro invertido.")

    # 2. cartera sin deterioro
    cartera = saldo(df, "13")
    deterioro = abs(saldo(df, "1399"))
    if cartera > 0 and deterioro == 0:
        add("ALTA", "NIIF 9 / Seccion 11 - perdida crediticia esperada",
            f"Cartera por {cartera:,.2f} sin cuenta de deterioro reconocida",
            "Calcular la perdida esperada por edades de cartera y reconocerla; revelar la politica.")

    # 3. inventarios sin ajuste a VNR
    inv = saldo(df, "14")
    det_inv = abs(saldo(df, "1499"))
    if inv > 0 and det_inv == 0:
        add("MEDIA", "NIC 2 / Seccion 13 - inventarios",
            f"Inventario por {inv:,.2f} sin ajuste a valor neto realizable",
            "Comparar costo vs. VNR y castigar obsoletos o de lenta rotacion.")

    # 4. PPE sin depreciacion del periodo
    ppe = saldo(df, "15")
    dep_acum = abs(saldo(df, "1592"))
    gasto_dep = saldo(df, "5160", "5260", "5165")
    if ppe > 0 and gasto_dep == 0:
        add("ALTA", "NIC 16 / Seccion 17 - propiedades planta y equipo",
            f"PPE por {ppe:,.2f} sin gasto de depreciacion en el periodo",
            "Verificar el calculo mensual, la vida util y el valor residual de cada activo.")
    if ppe > 0 and dep_acum == 0:
        add("MEDIA", "NIC 16 / Seccion 17",
            "No hay depreciacion acumulada registrada", "Revisar la politica de depreciacion.")

    # 5. anticipos y partidas puente
    for pref, etiqueta in [("1330", "Anticipos y avances"), ("1355", "Anticipo de impuestos"),
                           ("1365", "Cuentas por cobrar a trabajadores"),
                           ("1380", "Deudores varios"), ("2335", "Costos y gastos por pagar")]:
        v = abs(saldo(df, pref))
        if v > 0:
            add("MEDIA", "Depuracion de saldos",
                f"{etiqueta} ({pref}) con saldo de {v:,.2f}",
                "Confirmar antiguedad y soporte; depurar lo que no se vaya a realizar.")

    # 6. impuesto diferido
    if saldo(df, "1900") == 0 and abs(saldo(df, "2725")) == 0 and abs(saldo(df, "2740")) == 0:
        add("MEDIA", "NIC 12 / Seccion 29 - impuesto a las ganancias",
            "No hay impuesto diferido activo ni pasivo reconocido",
            "Comparar bases contables y fiscales (PPE, deterioros, provisiones) y reconocer el diferido.")

    # 7. provisiones y beneficios a empleados
    if abs(saldo(df, "26")) == 0:
        add("MEDIA", "NIC 37 / Seccion 21 - provisiones y contingencias",
            "No hay provisiones reconocidas",
            "Documentar litigios y obligaciones probables; revelar los pasivos contingentes.")
    if abs(saldo(df, "25")) == 0 and saldo(df, "5105", "5205") > 0:
        add("ALTA", "NIC 19 / Seccion 28 - beneficios a empleados",
            "Hay gasto de nomina pero no hay pasivo por beneficios a empleados",
            "Causar prestaciones sociales consolidadas al cierre.")

    # 8. concentracion del gasto
    gastos = df[df["clase"] == "5"].copy()
    total_g = gastos["saldo_final"].sum()
    if total_g > 0:
        top = gastos.nlargest(1, "saldo_final").iloc[0]
        part = top["saldo_final"] / total_g * 100
        if part > 40:
            add("BAJA", "Analisis de razonabilidad",
                f"La cuenta {top['codigo_puc']} {top['nombre_cuenta']} concentra el "
                f"{part:.1f}% del gasto",
                "Verificar que no haya gastos mal clasificados en esa cuenta.")

    if not A:
        add("BAJA", "-", "No se detectaron alertas con las reglas configuradas",
            "Complemente con pruebas sustantivas sobre las partidas materiales.")
    return pd.DataFrame(A)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("balance")
    ap.add_argument("--salida", default="salidas/analisis_balance.xlsx")
    args = ap.parse_args()

    df = cargar(Path(args.balance))
    val, ind, ale = validaciones(df), indicadores(df), alertas(df)
    por_clase = (df.groupby("clase_nombre")["saldo_final"].sum().round(2)
                 .reset_index().rename(columns={"saldo_final": "saldo"}))
    por_grupo = (df.groupby(["clase_nombre", "grupo"])["saldo_final"].sum().round(2)
                 .reset_index().rename(columns={"saldo_final": "saldo"}))

    salida = Path(args.salida)
    salida.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(salida, engine="openpyxl") as w:
        val.to_excel(w, sheet_name="Validaciones", index=False)
        ind.to_excel(w, sheet_name="Indicadores", index=False)
        ale.to_excel(w, sheet_name="Alertas tecnicas", index=False)
        por_clase.to_excel(w, sheet_name="Saldos por clase", index=False)
        por_grupo.to_excel(w, sheet_name="Saldos por grupo", index=False)
        df.to_excel(w, sheet_name="Balance clasificado", index=False)

    print("=" * 74, "\nVALIDACIONES\n" + "-" * 74)
    for _, r in val.iterrows():
        print(f"{r['validacion']:<58} {r['valor']:>14,.2f} {r['estado']}")
    print("\nINDICADORES\n" + "-" * 74)
    for _, r in ind.iterrows():
        v = f"{r['valor']:,.2f}" if isinstance(r["valor"], (int, float)) else "n/a"
        print(f"{r['indicador']:<38} {v:>18} {r['unidad']:<6} {r['referencia']}")
    print("\nALERTAS TECNICAS\n" + "-" * 74)
    for _, r in ale.iterrows():
        print(f"[{r['nivel']:<5}] {r['hallazgo']}\n         {r['norma']}\n         -> {r['accion_sugerida']}")
    print(f"\nArchivo generado: {salida}")


if __name__ == "__main__":
    main()
