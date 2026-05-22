# ---------------------------------------------------
# SELECCIÓN DEL NÚMERO DE PASOS
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# Definimos la función f(x) = cos(x)
def f(x):
    return np.cos(x)


# ---------------------------------------------------
# DATOS DEL PROBLEMA
# Límites de integración
a = 0
b = np.pi / 2


# ---------------------------------------------------
# VALOR EXACTO
# Integral exacta de cos(x) entre 0 y pi/2
valor_exacto = 1


# ---------------------------------------------------
# NÚMERO DE PASOS
# Diferentes valores de n
pasos = [2, 4, 8, 16]

# Lista para guardar errores
errores = []


# ---------------------------------------------------
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------

for n in pasos:

# ---------------------------------------------------
# Calculamos el ancho del intervalo
    h = (b - a) / n

# ---------------------------------------------------
# Generamos puntos
    x = np.linspace(a, b, n + 1)

    # Evaluamos la función
    y = f(x)

# ---------------------------------------------------
# Fórmula del trapecio
    suma = y[0] + y[-1]

    for i in range(1, n):
        suma += 2 * y[i]

    integral = (h / 2) * suma

    # Calculamos el error
    error = abs(valor_exacto - integral)

    # Guardamos el error
    errores.append(error)

    print("\nNúmero de pasos:", n)

    print("Aproximación:")
    print(integral)

    print("Error:")
    print(error)


# ---------------------------------------------------
# GRÁFICA
# ---------------------------------------------------
plt.plot(pasos, errores,
         marker='o')

plt.title("Error según el Número de Pasos")

plt.xlabel("Número de pasos")
plt.ylabel("Error")

plt.grid(True)

plt.show()