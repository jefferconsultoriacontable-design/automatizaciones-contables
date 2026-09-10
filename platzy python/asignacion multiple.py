X, Y, Z = "manzana", "naranja", "banana"
print(X,Y,Z)

A = B = C = "mandarina"
print(A,B,C)

print("mi fruta favorita es la " + X)
print(A + " " + Z)

a = 100
b = 250
c = 1650
print(a + b + c)

factura = 1560300
iva = 0.19 # 19% iva de la FE
retefuente = 0.025 # 2.5% RETEFUENTE POR COMPRAS 
descuento  =   0.10 # 10% DESCUENTO POR PRONTO PAGO

valor_iva = factura * iva
valor_descuento = factura * descuento
valor_retefuente = factura * retefuente

# Total neto a pagar
TOTAL = factura + valor_iva - valor_descuento - valor_retefuente

print(f"Base factura:     ${factura:,.2f}")
print(f"(+) IVA 19%:       ${valor_iva:,.2f}")
print(f"(-) Descuento 10%: ${valor_descuento:,.2f}")
print(f"(-) ReteFuente 2.5%:${valor_retefuente:,.2f}")
print("-" * 35)
print(f"TOTAL A PAGAR:    ${TOTAL:,.2f}")

factura = 1650306000
iva = 0.19 # 19%
retefuente = 0.025 # 2.5%
decuento = 0.25 # 25%

valor_factura = factura * iva
valor_descuento = factura * descuento
valor_retefuente = factura * retefuente

# Total neto a pagar
TOTAL = factura + valor_iva - valor_descuento - valor_retefuente

print(f"base factura:      ${factura:,.2f}")
print(f"(+) IVA 19%:       ${valor_iva:,.2f}")
print(f"(-) Descuento 25%: ${valor_descuento:,.2f}")
print(f"(-) ReteFuente 2.5%:${valor_retefuente:,.2f}")
print("-" * 35)
print(f"TOTAL A PAGAR:    ${TOTAL:,.2f}")

factura = 165030600000
iva = 0.19 # 19%

total_factura = factura * iva

# total neto a pagar

total = TOTAL * iva

print(f"(+)iva del 19%:${valor_iva:,.2f}")

