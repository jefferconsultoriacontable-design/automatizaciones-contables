# Lista de valores de facturas brutas de un cliente
facturas_clientes = [45000000, 120000000, 15000000, 85000000, 230000000]

# 1. Lógica tradicional corregida (con bucle for explícito)
retenciones_tradicional = []
for factura in facturas_clientes:
    if factura > 100000000:
        retenciones_tradicional.append(factura * 0.10)  # 10% para > 100M
    else:
        retenciones_tradicional.append(0.0)

# 2. Lógica profesional con List Comprehension (Mismo criterio: > 100M al 10%)
retenciones_optimizadas = [v * 0.10 if v > 100000000 else 0.0 for v in facturas_clientes]

print("Retenciones con bucle tradicional:", retenciones_tradicional)
print("Retenciones optimizadas (List Comp):", retenciones_optimizadas)