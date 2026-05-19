try:
    n = int(input("Ingrese la cantidad de valores a analizar: "))
except ValueError:
    print("Entrada inválida")
    exit()

if n <= 0:
    print("El número debe ser mayor que 0")
    exit()

enteros = []
flotantes = []
cadenas = []
booleanos = []

for i in range(n):
    valor = input("Ingrese un valor: ")

    # intentar entero
    try:
        v = int(valor)
        enteros.append(v)
        continue
    except ValueError:
        pass

    # intentar flotante
    try:
        v = float(valor)
        flotantes.append(v)
        continue
    except ValueError:
        pass

    # booleanos
    if valor.lower() == "true":
        booleanos.append(True)
        continue
    elif valor.lower() == "false":
        booleanos.append(False)
        continue

    # si no es nada anterior → cadena
    cadenas.append(valor)

print("Enteros:", enteros)
print("Flotantes:", flotantes)
print("Booleanos:", booleanos)
print("Cadenas:", cadenas)