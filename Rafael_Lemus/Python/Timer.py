import time

inicio = time.time()

suma = 0
for i in range(1, 101):
    suma += i

fin = time.time()

print("Suma:", suma)
print("Tiempo de ejecución:", fin - inicio, "segundos")