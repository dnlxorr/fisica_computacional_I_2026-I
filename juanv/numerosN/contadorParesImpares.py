n = int(input("Ingrese un numero entero positivo: "))

par = []
imp = []
lista = list(range(0, n+1))
print("La lista numeros", lista)

for i in range(0, n + 1):


    if i % 2 == 0:
        par.append(i)
    else:
        imp.append(i)


print("Pares:", par)
print("Impares:", imp)
print("Cantidad de Pares:", len(par))
print("Cantidad de Impares:", len(imp))
