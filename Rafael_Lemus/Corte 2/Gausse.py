import numpy as np
import matplotlib.pyplot as plt
from numpy.polynomial.legendre import leggauss

# Función a integrar
def f(x):
    return np.exp(-x**2)

# Cuadratura de Gauss-Legendre
def gauss_legendre(f, a, b, n):

    # Obtener nodos y pesos
    xi, wi = leggauss(n)

    # Transformación del intervalo [-1,1] -> [a,b]
    x_transformado = 0.5 * (b - a) * xi + 0.5 * (a + b)

    # Evaluar función transformada
    fx = f(x_transformado)

    # Fórmula de cuadratura
    integral = 0.5 * (b - a) * np.sum(wi * fx)

    return integral

# Intervalo de integración
a = 0
b = 1

# Valor de referencia
# Aproximación muy precisa usando muchos puntos
valor_exacto = gauss_legendre(f, a, b, 50)

# Distintos números de puntos
n_values = np.arange(2, 11)

# Lista de errores
errores = []

# Calcular aproximaciones
for n in n_values:

    aproximacion = gauss_legendre(f, a, b, n)

    error = abs(valor_exacto - aproximacion)

    errores.append(error)

    print(f"n = {n}")
    print(f"Integral ≈ {aproximacion:.12f}")
    print(f"Error = {error:.2e}")
    print()

# -----------------------------
# Gráfica del error
# -----------------------------
plt.figure(figsize=(8,5))

plt.plot(n_values, errores, 'o-')

plt.yscale('log')

plt.title('Convergencia de la Cuadratura de Gauss')
plt.xlabel('Número de puntos')
plt.ylabel('Error absoluto')
plt.grid(True)

plt.show()