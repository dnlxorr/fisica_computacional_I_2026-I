# ---------------------------------------------------
# INTEGRACIÓN MÚLTIPLE EN PYTHON
# ---------------------------------------------------

# Importamos NumPy
# Esta librería sirve para hacer cálculos matemáticos
import numpy as np


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------
# f(x,y) = sin(x) + cos(y)

def f(x, y):
    return np.sin(x) + np.cos(y)


# ---------------------------------------------------
# LÍMITES DE INTEGRACIÓN
# ---------------------------------------------------
# Región:
# 0 <= x <= 1
# 0 <= y <= 1

a, b = 0, 1
c, d = 0, 1


# ---------------------------------------------------
# MÉTODO DE RIEMANN
# ---------------------------------------------------
# Divide la región en pequeños cuadrados
# y suma las áreas.

def riemann(n):

    # Creamos puntos en x y y
    x = np.linspace(a, b, n)
    y = np.linspace(c, d, n)

    # Tamaño de cada división
    dx = (b - a) / (n - 1)
    dy = (d - c) / (n - 1)

    # Variable acumuladora
    suma = 0

    # Recorremos todos los puntos
    for xi in x:
        for yj in y:

            # función × área pequeña
            suma += f(xi, yj) * dx * dy

    return suma


# ---------------------------------------------------
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------
# Usa trapecios para aproximar el área.

def trapecio(n):

    # Creamos puntos
    x = np.linspace(a, b, n)
    y = np.linspace(c, d, n)

    # Creamos la malla
    X, Y = np.meshgrid(x, y)

    # Evaluamos la función
    Z = f(X, Y)

    # Aplicamos el método del trapecio
    return np.trapezoid(np.trapezoid(Z, x), y)


# ---------------------------------------------------
# MÉTODO MONTE CARLO
# ---------------------------------------------------
# Usa puntos aleatorios para aproximar
# la integral.

def montecarlo(N):

    # Generamos puntos aleatorios
    x_rand = np.random.uniform(a, b, N)
    y_rand = np.random.uniform(c, d, N)

    # Evaluamos la función
    valores = f(x_rand, y_rand)

    # Área de la región
    area = (b - a) * (d - c)

    # Promedio × área
    return area * np.mean(valores)


# ---------------------------------------------------
# RESULTADOS
# ---------------------------------------------------

print("Resultado con Riemann:")
print(riemann(50))

print("\nResultado con Trapecio:")
print(trapecio(50))

print("\nResultado con Monte Carlo:")
print(montecarlo(10000))


# ---------------------------------------------------
# VALOR EXACTO
# ---------------------------------------------------

# Integral exacta de:
# sin(x) + cos(y)

valor_exacto = (1 - np.cos(1)) + np.sin(1)

print("\nValor exacto aproximado:")
print(valor_exacto)