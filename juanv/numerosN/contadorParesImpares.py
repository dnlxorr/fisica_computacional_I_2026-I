# Pedir un número entero positivo
n = int(input("Ingrese un número entero positivo: "))

pares = 0
impares = 0

print("Lista de números:")

for i in range(1, n + 1):
    print(i)

    if i % 2 == 0:
        pares += 1
    else:
        impares += 1

print("Cantidad de números pares:", pares)
print("Cantidad de números impares:", impares)
