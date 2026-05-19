print(" TIPOS DE DATOS ")

def mostrar_dato(nombre, valor):
    print(f"{nombre}:", valor)
    print("Tipo:", type(valor))
    print()

# ENTERO
edad = 21
mostrar_dato("Edad", edad)

# DECIMAL
altura = 1.75
mostrar_dato("Altura", altura)

# COMPLEJO
numero_complejo = 2 + 3j
mostrar_dato("Número complejo", numero_complejo)

# TEXTO
mensaje = "Hola, estoy aprendiendo Python"
mostrar_dato("Mensaje", mensaje)

# BOOLEANO
es_estudiante = True
mostrar_dato("¿Es estudiante?", es_estudiante)

# LISTA
numeros = [1, 2, 3, 4]
numeros.append(5)
mostrar_dato("Lista", numeros)

# TUPLA
coordenadas = (10, 20)
mostrar_dato("Tupla", coordenadas)

# DICCIONARIO
persona = {"nombre": "Ana", "edad": 22}
mostrar_dato("Diccionario", persona)

# CONJUNTO
valores = {1, 2, 2, 3}
mostrar_dato("Conjunto", valores)