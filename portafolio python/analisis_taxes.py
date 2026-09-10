import pandas as pd
import numpy as np

# 1. Base de cartera
data = {
    'nit_cliente': ['9001', '8002', '7003', '6004', '5005'],
    'saldo_factura': [5000000, 12000000, 25000000, 8000000, 45000000],
    'dias_vencimiento': [0, 15, 45, 75, 120]
}
cartera_clientes = pd.DataFrame(data)

# 2. Definición de condiciones por rangos de vencimiento
condiciones = [
    cartera_clientes['dias_vencimiento'] <= 0,
    (cartera_clientes['dias_vencimiento'] > 0) & (cartera_clientes['dias_vencimiento'] <= 30),
    (cartera_clientes['dias_vencimiento'] > 30) & (cartera_clientes['dias_vencimiento'] <= 60),
    (cartera_clientes['dias_vencimiento'] > 60) & (cartera_clientes['dias_vencimiento'] <= 90),
    cartera_clientes['dias_vencimiento'] > 90
]

# 3. Asignación masiva de Clasificación y Acciones de Cobranza
etiquetas_riesgo = ['Al día', 'Leve', 'Moderado', 'Grave', 'Crítico']
acciones_cobranza = [
    "Sin acción",
    "Recordatorio suave",
    "Llamada inmediata",
    "Llamada inmediata",
    "Bloqueo de crédito y cobro jurídico"
]

cartera_clientes['Clasificacion_Riesgo'] = np.select(condiciones, etiquetas_riesgo, default='Indefinido')
cartera_clientes['Accion_Cobranza'] = np.select(condiciones, acciones_cobranza, default='Revisión manual')

print(cartera_clientes[['nit_cliente', 'dias_vencimiento', 'Clasificacion_Riesgo', 'Accion_Cobranza']])