import time

# Tiempo inicial
inicio = time.time()

# Programa: suma de números de 1 hasta 100000
suma = 0
for i in range(1, 100001):
    suma += i

# Tiempo final
fin = time.time()

# Tiempo total de ejecución
tiempo_ejecucion = fin - inicio

print("Resultado de la suma:", suma)
print("Tiempo de ejecución:", tiempo_ejecucion, "segundos")