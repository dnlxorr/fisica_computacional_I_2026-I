import time

inicio = time.time()

suma = 0

for i in range(1, 1001):
    suma += i
    print(f"Suma hasta {i} = {suma}")

duracion = time.time() - inicio

print("La suma total es:", suma)
print("Tiempo de ejecución:", duracion)