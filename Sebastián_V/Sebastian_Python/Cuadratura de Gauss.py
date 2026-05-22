import numpy as np
from scipy.integrate import fixed_quad

# Definir la función a integrar
def f(x):
    return x**2

# Intervalo de integración
a, b = 0, 2

# Aplicar cuadratura de Gauss (n=2 puntos)
resultado, _ = fixed_quad(f, a, b, n=2)

print(f"Resultado con cuadratura de Gauss: {resultado:.4f}")
print(f"Valor exacto: 8/3 ≈ {8/3:.4f}")
print(f"Error absoluto: {abs(resultado - 8/3):.6f}")


# -----------------------------
# función a integrar
# -----------------------------
def f(x):
    return x**2

# -----------------------------
# cuadratura Gauss-Legendre manual
# en [-1, 1]
# -----------------------------
def gauss_legendre_2pt(f, a, b):
    """
    Implementación explícita con 2 puntos de Gauss-Legendre
    """

    # nodos y pesos para n=2 en [-1,1]
    nodos = np.array([-1/np.sqrt(3), 1/np.sqrt(3)])
    pesos = np.array([1, 1])

    # cambio de variable de [-1,1] a [a,b]
    def transform(xi):
        return (b - a)/2 * xi + (a + b)/2

    integral = 0.0

    for xi, wi in zip(nodos, pesos):
        x = transform(xi)
        integral += wi * f(x)

    # factor de escala del cambio de intervalo
    integral *= (b - a)/2

    return integral


# -----------------------------
# evaluación
# -----------------------------
a, b = 0, 2
resultado = gauss_legendre_2pt(f, a, b)

print("Resultado Gauss manual:", resultado)
print("Exacto:", 8/3)
print("Error:", abs(resultado - 8/3))
