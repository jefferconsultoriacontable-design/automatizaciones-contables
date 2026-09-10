edad_maria = 56
edad_alberto = 47
altura_maria = 1.56
altura_alberto = 1.70

# si maria es mayor que alberto entonces

if (edad_maria > edad_alberto):
  print('maria tiene mas años que alberto')

  if (altura_maria > altura_alberto):
    print('adicionalmente, es mas alta que alberto')

  else:
    print('sin embargo alberto es mas alto.')

    # de lo contrario:
else:
  print('de lo Contrario alberto es mas alto')

# ejemplo listas de activos corrientes
lista = ["caja", "banco", "clientes", "activo corriente"]
for lista in lista:
  print(lista)

# ejemplo 2 pythonero open ai

for i in range(12000,650000,980000):
 print(i**2)

# pythonero de open ai es canson

cuentas_financieras = {
    "caja": 12500,
    "inventario": 160000,
    "clientes": 17800,       # Corregido el typo 'cientes'
    "bancos": 102000,
    "bancos_colombia": 16000000,
    "bancos_españa": 1700000000
}

# Iterar clave-valor es el estándar para auditar saldos programáticamente
for cuenta, saldo in cuentas_financieras.items():
    print(f"Cuenta: {cuenta} - Saldo: {saldo:,.2f}")


