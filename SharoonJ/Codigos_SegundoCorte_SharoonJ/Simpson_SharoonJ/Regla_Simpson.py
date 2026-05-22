# ---------------------------------------------------
# REGLA DE SIMPSON
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------

# Definimos la función f(x) = sen(x)
def f(x):
    return np.sin(x)


# ---------------------------------------------------
# DATOS DEL PROBLEMA
# ---------------------------------------------------

# Límite inferior
a = -np.pi

# Límite superior
b = np.pi

# Número de intervalos
# Debe ser PAR para aplicar Simpson
n = 6


# ---------------------------------------------------
# CÁLCULO DEL ANCHO DE CADA INTERVALO
h = (b - a) / n


# ---------------------------------------------------
# GENERACIÓN DE PUNTOS
# Creamos los puntos del intervalo
x = np.linspace(a, b, n + 1)

# Evaluamos la función en cada punto
y = f(x)


# ---------------------------------------------------
# APLICACIÓN DE LA REGLA DE SIMPSON
# ---------------------------------------------------
# Iniciamos la suma con el primer y último valor
suma = y[0] + y[-1]

# Sumamos índices impares multiplicados por 4
for i in range(1, n, 2):
    suma += 4 * y[i]

# Sumamos índices pares multiplicados por 2
for i in range(2, n - 1, 2):
    suma += 2 * y[i]

# Aplicamos la fórmula final de Simpson
integral = (h / 3) * suma


# ---------------------------------------------------
# RESULTADO
print("Resultado aproximado de la integral:")
print(integral)


# ---------------------------------------------------
# GRÁFICA
# ---------------------------------------------------
x_grafica = np.linspace(a, b, 200)
y_grafica = f(x_grafica)

plt.plot(x_grafica, y_grafica, label='f(x) = sen(x)')

plt.plot(x, y, 'o')

plt.fill_between(x, y, alpha=0.3)

plt.title("Regla de Simpson")

plt.xlabel("x")
plt.ylabel("f(x)")

plt.grid(True)

plt.legend()
plt.show()