import pandas as pd
import numpy as np

# 1. Base consolidada con longitudes de arreglos idénticas (7 filas exactas)
data_transacciones = pd.DataFrame({
    'nit_del_cliente': ['900123456', '900123456', '900123456', '900123456', '900123456', '900123456', '900123456'], 
    'concepto': [
        'consignaciones bancarias', 
        'consumo tarjeta de credito', 
        'ingresos laborales', 
        'patrimonio_actual', 
        'patrimonio_anterior', 
        'pasivos_totales', 
        'costos_deducciones'
    ],
    'valor': [
        120000000,  # Consignaciones
        45000000,   # Consumos TC
        85000000,   # Ingresos laborales
        350000000,  # Patrimonio T
        300000000,  # Patrimonio T-1
        120000000,  # Pasivos
        30000000    # Costos/Deducciones
    ]
})

print("--- Base de Datos Financiera Inicial ---")
print(data_transacciones)

# 2. Motor de análisis tributario y fiscal (Validación DIAN)
patrimonio_actual = data_transacciones.loc[data_transacciones['concepto'] == 'patrimonio_actual', 'valor'].values[0]
patrimonio_anterior = data_transacciones.loc[data_transacciones['concepto'] == 'patrimonio_anterior', 'valor'].values[0]
incremento_patrimonial = patrimonio_actual - patrimonio_anterior

ingresos_totales = data_transacciones.loc[
    data_transacciones['concepto'].isin(['consignaciones bancarias', 'ingresos laborales']), 'valor'
].sum()

consumos_tc = data_transacciones.loc[data_transacciones['concepto'] == 'consumo tarjeta de credito', 'valor'].values[0]
pasivos_totales = data_transacciones.loc[data_transacciones['concepto'] == 'pasivos_totales', 'valor'].values[0]

# Cálculo de Patrimonio Líquido
patrimonio_liquido = patrimonio_actual - pasivos_totales

# Indicador de liquidez fiscal y endeudamiento
ratio_endeudamiento = pasivos_totales / patrimonio_actual if patrimonio_actual > 0 else 0
alerta_endeudamiento = np.where(ratio_endeudamiento > 0.5, "Riesgo de iliquidez fiscal", "Saludable")

# Reglas de validación exógena
alerta_consumos = np.where(consumos_tc > ingresos_totales, "Alerta: Consumos de TC superan ingresos declarados", "Normal")

print(f"\n--- Diagnóstico Fiscal y Patrimonial ---")
print(f"Ingresos Totales (Base Renta): ${ingresos_totales:,.2f}")
print(f"Incremento Patrimonial: ${incremento_patrimonial:,.2f}")
print(f"Patrimonio Líquido: ${patrimonio_liquido:,.2f}")
print(f"Ratio de Endeudamiento: {ratio_endeudamiento:.2%} ({alerta_endeudamiento})")
print(f"Validación Tarjeta de Crédito: {alerta_consumos}")

