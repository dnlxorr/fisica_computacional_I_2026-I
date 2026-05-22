# ---------------------------------------------------
# REGLA DEL TRAPECIO
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------
# f(x) = x²
def f(x):
    return x**2


# ---------------------------------------------------
# DATOS DEL PROBLEMA
# Límite inferior de integración
a = 0

# Límite superior de integración
b = 4

# Número de trapecios
n = 4


# ---------------------------------------------------
# CÁLCULO DEL ANCHO DE CADA TRAPECIO
h = (b - a) / n


# ---------------------------------------------------
# GENERAMOS LOS PUNTOS EN X
# Creamos los puntos del intervalo
x = np.linspace(a, b, n + 1)

# Evaluamos la función en cada punto
y = f(x)


# ---------------------------------------------------
# APLICACIÓN DE LA REGLA DEL TRAPECIO
# Iniciamos la suma con el primer y último valor
suma = y[0] + y[-1]

# Sumamos los valores internos multiplicados por 2
for i in range(1, n):
    suma += 2 * y[i]

# Aplicamos la fórmula final del trapecio
integral = (h / 2) * suma


# ---------------------------------------------------
# MOSTRAMOS EL RESULTADO
print("Resultado aproximado de la integral:")
print(integral)


# ---------------------------------------------------
# GRÁFICA
# ---------------------------------------------------


x_grafica = np.linspace(a, b, 100)
y_grafica = f(x_grafica)

plt.plot(x_grafica, y_grafica, label='f(x) = x²')


plt.fill_between(x, y, alpha=0.3)

# Dibujamos los puntos usados
plt.plot(x, y, 'o')

plt.title("Regla del Trapecio")
plt.xlabel("x")
plt.ylabel("f(x)")

plt.grid(True)

plt.legend()
plt.show()