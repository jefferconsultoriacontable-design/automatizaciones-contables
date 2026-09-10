import pandas as pd

# Corrección de sintaxis: Definición correcta de la estructura de datos (Auxiliar de Cartera)
clientes = pd.DataFrame({
    'nit_cliente': ['900111222', '800333444', '900555666', '890777888', '900999000'],
    'Dias_Vencidos': [30, 60, 90, 120, 150],
    'reportar_centrales_de_riesgo': [False, False, True, True, True]
})

import numpy as np
import pandas as pd

# Simulación de auxiliar de cartera (Cuentas por Cobrar)
cartera_clientes = pd.DataFrame({
    'nit_cliente': ['900111222', '800333444', '900555666', '890777888', '900999000'],
    'saldo_factura': [45000000, 120000000, 15000000, 85000000, 230000000],
    'dias_vencimiento': [15, 45, 120, 210, 5]
})

# Política de deterioro NIIF optimizada con vectorización (np.select)
condiciones = [
    cartera_clientes['dias_vencimiento'] <= 30,
    (cartera_clientes['dias_vencimiento'] > 30) & (cartera_clientes['dias_vencimiento'] <= 90),
    (cartera_clientes['dias_vencimiento'] > 90) & (cartera_clientes['dias_vencimiento'] <= 180),
    cartera_clientes['dias_vencimiento'] > 180
]

tasas_provision = [0.0, 0.05, 0.10, 0.50]

cartera_clientes['tasa_deterioro'] = np.select(condiciones, tasas_provision, default=0.0)
cartera_clientes['valor_provision'] = cartera_clientes['saldo_factura'] * cartera_clientes['tasa_deterioro']

print("--- Papel de Trabajo: Deterioro de Cartera (NIIF) ---")
print(cartera_clientes[['nit_cliente', 'saldo_factura', 'dias_vencimiento', 'valor_provision']])
print(f"\nProvisión Total Acumulada: ${cartera_clientes['valor_provision'].sum():,.2f}")