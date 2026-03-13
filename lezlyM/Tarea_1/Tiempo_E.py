print("Hello, World!")
import time

# 1. Capturamos el momento exacto antes de empezar
inicio = time.perf_counter()

# 2. La instrucción que queremos medir
print("Hello, World!")

# 3. Capturamos el momento exacto al terminar
fin = time.perf_counter()

# 4. Calculamos la diferencia
tiempo_total = fin - inicio

print(f"\n--- Estadísticas ---")
print(f"El código tardó: {tiempo_total:.8f} segundos")