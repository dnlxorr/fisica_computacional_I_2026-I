n = int(input("Ingrese un número: "))

num = []

for i in range(0, n+1):
    num.append(i)

primo = []
pares = []
impares = []

for i in num:

    if i % 2 == 0:
        pares.append(i)
    else:
        impares.append(i)

    if i > 1:
        esPrimo = True

        for j in range(2, i):
            if i % j == 0:
                esPrimo = False
                break

        if esPrimo:
            primo.append(i)

print("Numeros pares:", pares)
print("Cantidad de pares:", len(pares))

print("Numeros impares:", impares)
print("Cantidad de impares:", len(impares))

print("Numeros primos:", primo)
print("Cantidad de primos:", len(primo))