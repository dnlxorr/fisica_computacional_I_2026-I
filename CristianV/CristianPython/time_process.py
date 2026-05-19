import time

# 1. Guardar el tiempo de inicio
inicio = time.perf_counter()

# --- AQUÍ VA TU CÓDIGO ---
# Ejemplo: un bucle simple que suma números
suma = 0
for i in range(1000):
    suma += i
# -------------------------

# 2. Guardar el tiempo de finalización
fin = time.perf_counter()

# 3. Calcular la diferencia
tiempo_ejecucion = fin - inicio

print(f"El código tardó {tiempo_ejecucion:.4f} segundos en ejecutarse.")