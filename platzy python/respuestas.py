# ind   01234
texto = "Este es un texto"

print(texto[:-2])

curso = "Este curso es de javascrip, javascrip"
print(curso.replace("javascrip", "python"))

textoDividido = texto.split()

print(textoDividido)

# Normalización

texto2 = "Este texto tiene MAYUSCULAS y minusculas y necesito encontrar ciertas palabras"

print("mayusculas".lower() in texto2.lower())