import random

numero = random.randrange(1,100)
print(numero)
print(type(numero))


import random

numero = random.randrange(1, 101)

print(numero)

if numero % 2 == 0:
    print("El número es par")
else:
    print("El número es impar")

saldo = 15000000

if saldo > 1000000:
    print("revisar saldo")
else:
    print("saldo dentro del rango")