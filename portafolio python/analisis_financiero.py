import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

print("¡Motor analítico y contable inicializado correctamente! 🚀\n")

# --- 1. ESTADOS FINANCIEROS COMPARATIVOS (VECTORIZADO) ---
datos_financieros = {
    'Escenario': ['Base', 'Proyección'],
    'Ingresos': [80_000_000_000, 800_000_000_000],
    'Costos': [300_000_000, 300_000_000],
    'Gastos': [200_000_000, 40_000_000_000],
    'Activos': [50_000_000_000_000, 5_000_000_000],
    'Pasivos': [10_000_000_000_000, 1_500_000_000]
}

df_fin = pd.DataFrame(datos_financieros)
df_fin['Utilidad Neta'] = df_fin['Ingresos'] - df_fin['Costos'] - df_fin['Gastos']
df_fin['Patrimonio'] = df_fin['Activos'] - df_fin['Pasivos']
df_fin['Margen Neto'] = df_fin['Utilidad Neta'] / df_fin['Ingresos']
df_fin['Endeudamiento'] = df_fin['Pasivos'] / df_fin['Activos']

print("--- 1. Resumen Financiero Ejecutivo ---")
print(df_fin[['Escenario', 'Ingresos', 'Utilidad Neta', 'Margen Neto', 'Endeudamiento']].to_string(index=False))


# --- 2. CONTROL PATRIMONIAL Y SARLAFT ---
patrimonio_neto = df_fin.loc[df_fin['Escenario'] == 'Base', 'Patrimonio'].values[0]

if patrimonio_neto >= 1_500_000_000:
    alerta_sarlaft = "ALERTA ROJA: Posible riesgo de lavado de activos (Revisión DIAN/UIAF)."
elif patrimonio_neto <= 15_000_000:
    alerta_sarlaft = "Perfil Bajo: No cumple umbrales de fiscalización."
else:
    alerta_sarlaft = "Rango Operativo Estándar."

print(f"\n--- 2. Control SARLAFT ---")
print(f"Patrimonio Base Evaluado: ${patrimonio_neto:,.2f} -> {alerta_sarlaft}")


# --- 3. AUDITORÍA TRIBUTARIA IVA 2026 ---
df_iva = pd.DataFrame([
    {"Bimestre": "B1", "Valor": 9_956_000_000, "Estado": "Presentado"},
    {"Bimestre": "B2", "Valor": 15_600_000_000, "Estado": "Presentado"},
    {"Bimestre": "B3", "Valor": 23_650_003_000, "Estado": "Presentado"},
    {"Bimestre": "B4", "Valor": 35_060_004_000, "Estado": "Presentado"},
    {"Bimestre": "B5", "Valor": None, "Estado": "Pendiente"}
])

total_presentado = df_iva.loc[df_iva['Estado'] == 'Presentado', 'Valor'].sum()
pendientes = df_iva[df_iva['Estado'] == 'Pendiente']

print(f"\n--- 3. Auditoría Tributaria IVA ---")
print(f"Total IVA Presentado ante la DIAN: ${total_presentado:,.2f}")

if not pendientes.empty:
    print(f"⚠️ AUDITORÍA: Hay {len(pendientes)} periodo(s) pendiente(s):")
    print(pendientes[['Bimestre', 'Estado']].to_string(index=False))


# --- 4. TOPES DIAN & OBLIGACIÓN DE RENTA (UVT) ---
uvt = 49799
tope_1400_uvt = 1400 * uvt  
tope_patrimonio_uvt = 4500 * uvt  # $237,375,000 aprox

patrimonio_bruto = 224_096_000
compras_anuales = 69_718_600
tarjetas_credito = 69_718_600
movimientos_bancarios = 69_718_600

obliga_patrimonio = patrimonio_bruto >= tope_patrimonio_uvt
obliga_transacciones = (
    (compras_anuales >= tope_1400_uvt) or 
    (tarjetas_credito >= tope_1400_uvt) or 
    (movimientos_bancarios >= tope_1400_uvt)
)

print(f"\n--- 4. Validación Declaración de Renta ---")
print(f"Tope 1400 UVT: ${tope_1400_uvt:,.2f}")
print(f"¿Supera tope de patrimonio?: {obliga_patrimonio}")
print(f"¿Supera topes de consumos/consignaciones?: {obliga_transacciones}")
print(f"-> ¿Obligado a declarar renta?: {obliga_patrimonio or obliga_transacciones}")


# --- 5. INTELIGENCIA ARTIFICIAL: DETECCIÓN DE ANOMALÍAS ---
np.random.seed(42)
monto_normal = np.random.normal(loc=1_500_000, scale=400_000, size=1000)
hora_normal = np.random.randint(low=8, high=18, size=1000)

df_diario = pd.DataFrame({
    'Transaccion_ID': range(1001, 2001),
    'Monto_COP': monto_normal,
    'Hora_Registro': hora_normal
})

anomalias = pd.DataFrame({
    'Transaccion_ID': [9901, 9902, 9903],
    'Monto_COP': [850_000_000, 2_000, 450_000_000],
    'Hora_Registro': [2, 3, 23]
})

df_audit = pd.concat([df_diario, anomalias], ignore_index=True)

X = df_audit[['Monto_COP', 'Hora_Registro']]
modelo = IsolationForest(contamination=0.005, random_state=42)
df_audit['Es_Anomalia'] = modelo.fit_predict(X)

hallazgos = df_audit[df_audit['Es_Anomalia'] == -1].copy()
hallazgos['Monto_Formateado'] = hallazgos['Monto_COP'].apply(lambda x: f"${x:,.2f}")

print(f"\n--- 5. Reporte de Auditoría IA (Hallazgos) ---")
print(hallazgos[['Transaccion_ID', 'Hora_Registro', 'Monto_Formateado']].to_string(index=False))

import pandas as pd

def detectar_facturacion_fragmentada(df):
    # Agrupamos por Fecha y NIT, sumando el valor y contando cuántos registros hay
    resumen = df.groupby(['Fecha', 'NIT_Tercero']).agg(
        Valor_Total=('Valor_Debito', 'sum'),
        Cantidad_Transacciones=('Valor_Debito', 'count')
    ).reset_index()
    
    # Filtramos la "maña": más de 2 transacciones al mismo tercero el mismo día
    sospechosos = resumen[resumen['Cantidad_Transacciones'] >= 3]
    
    # Cruzamos de vuelta con el diario para ver el detalle de los asientos fraccionados
    alerta_fraude = df.merge(sospechosos[['Fecha', 'NIT_Tercero']], on=['Fecha', 'NIT_Tercero'])
    
    return alerta_fraude