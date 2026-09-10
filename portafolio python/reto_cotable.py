import pandas as pd

# 1. Definición correcta de la estructura contable (separando código y descripción)
df_cuentas = pd.DataFrame({
    'Codigo_Cuenta': [11050501, 11100502, 11100503, 11100504, 11100505],
    'Nombre_Cuenta': ['CAJA GENERAL', 'BANCOLOMBIA', 'BANCO DAVIVIENDA', 'BANCOLOMBIA AHORROS', 'BANCO DE BOGOTA'],
    'Saldo': [1500000, 45000000, 12000000, 8500000, 3100000]
})

print("--- Plan de Cuentas Inicial ---")
print(df_cuentas)

# 2. Aplicando filtro contable con Pandas (Activos disponibles > 10 millones)
efectivo_fuerte = df_cuentas[df_cuentas['Saldo'] > 10000000]

print("\n--- Cuentas con Liquidez Alta (> 10M) ---")
print(efectivo_fuerte)