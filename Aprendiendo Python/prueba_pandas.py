import pandas as pd
import numpy as np

# 1. Definición de cifras base (Estado de Resultados y Balance)
ingresos = 800000000
costos = 300000000
gastos = 200000000
activos = 50000000000000
pasivos = 10000000000000

# 2. Funciones de cálculo financiero
def calcular_utilidad_neta(ing, cos, gas):
    return ing - cos - gas

def calcular_patrimonio(act, pas):
    return act - pas

# 3. Ejecución de cálculos clave
utilidad_neta = calcular_utilidad_neta(ingresos, costos, gastos)
patrimonio = calcular_patrimonio(activos, pasivos)
margen_neto = (utilidad_neta / ingresos) * 100 if ingresos > 0 else 0
endeudamiento = (pasivos / activos) * 100 if activos > 0 else 0

# Impuestos (ejemplo sobre una base gravable / valor de facturas)
valor_base = 6532650000
total_tasa_impuestos = 0.10 + 0.19 + 0.005 + 0.08  # Retención + IVA + ICA + Impoconsumo
impuestos = valor_base * total_tasa_impuestos
utilidad_neta_despues_impuestos = utilidad_neta - impuestos

# 4. Resultados en consola con formato contable
print(f"Utilidad antes de impuestos: ${utilidad_neta:,.2f}")
print(f"Impuestos calculados:       ${impuestos:,.2f}")
print(f"Utilidad neta post-impuestos: ${utilidad_neta_despues_impuestos:,.2f}")
print(f"Patrimonio contable:        ${patrimonio:,.2f}")
print(f"Margen Neto:                {margen_neto:.2f}%")
print(f"Nivel de Endeudamiento:     {endeudamiento:.2f}%")

# 5. Estructura de DataFrame limpia (longitudes idénticas)
data = {
    'Indicador': ['Periodo 1', 'Periodo 2 (Proyectado)'],
    'Ingresos': [ingresos, ingresos * 1.1],
    'Costos': [costos, costos * 1.05],
    'Gastos': [gastos, gastos * 1.02],
    'Utilidad Neta': [utilidad_neta, utilidad_neta * 1.15],
    'Patrimonio': [patrimonio, patrimonio * 1.08]
}

df_financiero = pd.DataFrame(data)
print("\n--- Resumen Financiero en DataFrame ---")
print(df_financiero)