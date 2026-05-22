# ---------------------------------------------------
# ERRORES DE INTEGRACION
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# FUNCIÓN A INTEGRAR
# Definimos la función f(x) = e^x
def f(x):
    return np.exp(x)

# ---------------------------------------------------
# DATOS DEL PROBLEMA
# ---------------------------------------------------
# Límites de integración
a = 0
b = 1

# Número de intervalos
n = 4

# ---------------------------------------------------
# VALOR EXACTO
# Integral exacta de e^x entre 0 y 1
valor_exacto = np.exp(1) - np.exp(0)

# ---------------------------------------------------
# PUNTOS
# Ancho de intervalo
h = (b - a) / n

# Puntos en x
x = np.linspace(a, b, n + 1)

# Valores de la función
y = f(x)

# ---------------------------------------------------
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------
suma_trapecio = y[0] + y[-1]

for i in range(1, n):
    suma_trapecio += 2 * y[i]

trapecio = (h / 2) * suma_trapecio


# ---------------------------------------------------
# MÉTODO DE SIMPSON
# ---------------------------------------------------
suma_simpson = y[0] + y[-1]

# Índices impares
for i in range(1, n, 2):
    suma_simpson += 4 * y[i]

# Índices pares
for i in range(2, n - 1, 2):
    suma_simpson += 2 * y[i]

simpson = (h / 3) * suma_simpson


# ---------------------------------------------------
# ERRORES
# ---------------------------------------------------
error_trapecio = abs(valor_exacto - trapecio)
error_simpson = abs(valor_exacto - simpson)


# ---------------------------------------------------
# RESULTADOS
print("VALOR EXACTO:")
print(valor_exacto)

print("\nTRAPECIO:")
print(trapecio)

print("Error:")
print(error_trapecio)

print("\nSIMPSON:")
print(simpson)

print("Error:")
print(error_simpson)


# ---------------------------------------------------
# GRÁFICAS
# Curva suave para la función original
x_suave = np.linspace(a, b, 200)
y_suave = f(x_suave)

# Creamos figura con 3 gráficas
fig, axs = plt.subplots(1, 3, figsize=(15, 4))


# ---------------------------------------------------
# GRÁFICA 1 - FUNCIÓN ORIGINAL
axs[0].plot(x_suave, y_suave, color='blue')

axs[0].set_title("Función Original")

axs[0].set_xlabel("x")
axs[0].set_ylabel("f(x)")

axs[0].grid(True)


# ---------------------------------------------------
# GRÁFICA 2 - TRAPECIO
axs[1].plot(x_suave, y_suave, color='black')

axs[1].plot(x, y,
            color='red',
            marker='o')

axs[1].fill_between(x, y,
                    color='red',
                    alpha=0.3)

axs[1].set_title("Método del Trapecio")

axs[1].set_xlabel("x")
axs[1].grid(True)


# ---------------------------------------------------
# GRÁFICA 3 - SIMPSON
axs[2].plot(x_suave, y_suave, color='black')

axs[2].plot(x, y,
            color='green',
            marker='s')

axs[2].fill_between(x, y,
                    color='green',
                    alpha=0.3)

axs[2].set_title("Método de Simpson")

axs[2].set_xlabel("x")
axs[2].grid(True)

plt.tight_layout()
plt.show()