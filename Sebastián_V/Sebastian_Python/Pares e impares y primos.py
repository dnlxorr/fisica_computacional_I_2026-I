entrada=int(input("Ingrese el número máximo :  "))
lista= list(range(0,entrada+1))
pares=[]
impares=[]
primos=[True]*(entrada+1)
primos[0]=False
primos[1]=False
lista_primos=[]
for n in range(0,entrada+1):
    if n%2==0:
        pares.append(n)
    else:
        impares.append(n)
for i in range(2, entrada+1):
    if primos[i] == True:
        for j in range(i*2, entrada +1, i):
            primos[j] = False
for i in range(2, entrada+1):
    if primos[i] == True:
        lista_primos.append(i)

print(f"La lista de números es: {lista} ")
print(f"los numero pares son:  {pares}")
print("La cantidad de números pares es: ", len(pares))
print(f"los numero impares son:  {impares}")
print("La cantidad de números impares es: ", len(impares))
print(f"Los números primos encontrados son: {lista_primos}")
print("La cantidad de números primos es: ", len(lista_primos))

