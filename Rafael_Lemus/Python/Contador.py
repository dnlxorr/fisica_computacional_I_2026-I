
try:
    n = int(input("Ingrese un número entero n: "))
except ValueError:
    print("Entrada inválida")
    exit()

if n < 0:
    print("El número debe ser mayor o igual a 0")
    exit()

enteros = []
pares = []
impares = []
primos = []

for i in range(n + 1):
    enteros.append(i)

    if i % 2 == 0:
        pares.append(i)
    else:
        impares.append(i)

    if i >= 2:
        primo = True
        for j in range(2, int(i**0.5) + 1):
            if i % j == 0:
                primo = False
                break
        if primo:
            primos.append(i)

print("Enteros:", enteros)
print("Pares:", pares)
print("Impares:", impares)
print("Primos:", primos)


