import numpy as np
import matplotlib.pyplot as plt

# Función a integrar
def f(x):
    return np.exp(-x)

# Valor exacto de la integral de 0 a 1
valor_exacto = 1 - np.exp(-1)

# Regla del trapecio
def trapecio(a, b, n):
    h = (b - a) / n
    suma = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        suma += f(a + i*h)

    return h * suma

# Intervalo de integración
a = 0
b = 1

# Tolerancia deseada
tolerancia = 1e-6

# Listas para almacenar resultados
n_values = []
errores = []

# Selección automática del número de pasos
n = 1

while True:

    aproximacion = trapecio(a, b, n)

    error = abs(valor_exacto - aproximacion)

    n_values.append(n)
    errores.append(error)

    # Verificar si se alcanzó la tolerancia
    if error < tolerancia:
        break
    n += 1

# Mostrar resultado final
print("Número óptimo de pasos:", n)
print("Integral aproximada:", aproximacion)
print("Valor exacto:", valor_exacto)
print("Error absoluto:", error)

# -----------------------------------
# Gráfica del error
# -----------------------------------
plt.figure(figsize=(8,5))

plt.plot(n_values, errores, 'o-')

plt.yscale('log')

plt.title('Selección del número de pasos')
plt.xlabel('Número de pasos (n)')
plt.ylabel('Error absoluto')
plt.grid(True)

plt.show()