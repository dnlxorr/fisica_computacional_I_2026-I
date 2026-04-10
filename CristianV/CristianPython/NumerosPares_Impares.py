entrada = input("Ingresa los números separados por espacios: ")

numeros = []

for valor in entrada.split():
    try:
        numeros.append(int(valor))
    except:
        print("Ingreso un caracter incompatible")

pares = []
impares = []
primos = []

contPares = 0
contImpares = 0

for n in numeros:
    if n % 2 == 0:
        pares.append(n)
    else:
        impares.append(n)

for m in numeros:
    if m > 1:
        es_primo = True
        for i in range(2, int(m ** 0.5) + 1): #Formula saca de google
            if m % i == 0:
                es_primo = False
                break

        if es_primo:
            primos.append(m)

print(f"La lista de numeros es:  {numeros}")
print(f"La lista de pares son: {pares}")
print(f"Los numeros pares son: ", len(pares))
print(f"La lista de impares son: {impares}")
print(f"Los numeros de impares es:", len(impares))
print(f"La lista de primos son: {primos}")
print(f"Los numeros primos son:", len(primos))