import time

inicio = time.time()

suma = 0

for i in range(1, 1001):
    suma = suma + i

fin = time.time()

tiempo = fin - inicio

print("La suma de los números del 1 al 1000 es:", suma)
print("Tiempo de ejecución:", tiempo, "segundos")
