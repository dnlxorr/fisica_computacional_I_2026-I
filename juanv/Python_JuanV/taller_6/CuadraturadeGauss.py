# ----------------------------------------------------------
# CUADRATURA DE GAUSS
# ----------------------------------------------------------
# Este método usa puntos especiales
# para aproximar integrales.
# ----------------------------------------------------------

import math

def f(x):

    return x**2


a = 0
b = 2

# Puntos de Gauss para 2 puntos
x1 = -0.577
x2 = 0.577

# Pesos
w1 = 1
w2 = 1

# Cambio de variable
punto1 = ((b - a) / 2) * x1 + ((b + a) / 2)
punto2 = ((b - a) / 2) * x2 + ((b + a) / 2)

# Fórmula de Gauss
integral = ((b - a) / 2) * (w1 * f(punto1) + w2 * f(punto2))

print("Integral aproximada:", integral)