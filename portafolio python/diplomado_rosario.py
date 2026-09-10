import pandas as pd

aptos = pd.read_csv("https://raw.githubusercontent.com/Fabian830348/Bases_Datos/refs/heads/master/apartamentos.csv")

# Auditoría rápida de tipos de datos y nulos
print(aptos.info())

# Vista previa de los primeros registros
print(aptos.head(3))

# calcula 
45+23-78+45*2

# calcular
print(34+45)
print(30-23)
print(34*34)


# calcular la siguientes operaciones
print(100/3)
print(23/5)
print(23//5) # división entera.
print(23%5)  # residuo

# ejemplo
2**10 + 5**4


print(round(4.543))     # 5.0
print(round(4.43))      # 4
print(round(6.4689,3))  # 6.469
print(round(3.125,2))   # 3.12


# observe lo siguiente: cuando es exactamente .5 : se envía al par más cercano.
print(round(4.545))
print(round(4.5))
print(round(5.5))
     
# hola este es un comentario

"""
cuando se quieren comentarios de
varias líneas en un bloque de código
se pueden usar comillas dobles
"""
34+89-12+34*90-4/9


# type sirve para mirar el tipo de dato
type(60)

print(type(67))
print(type("jeffer"))

print(type("67"))
print(type(45.9))


type(56+80)      # int
type(3.56-3.90)  # float #imprime el último.


# python ejecuta todo el código, pero muestra solo la última línea
type(45/7)
type(34*56)

print(type(56+80))
print(type(3.56-3.90) )
print(type("hola cómo están")) # el color es rojito
print(type(False))
print(type("False"))

print(type(45/7))
print(type(34*56))

print(type(False)) # color es azul
print(type(' hola, jeffer'))


# la suma concatena, es decir, pega las cadenas
print("fabian"+"python")



           


