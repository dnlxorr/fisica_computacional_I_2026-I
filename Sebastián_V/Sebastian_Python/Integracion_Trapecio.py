import numpy as np

# -----------------------------
# función a integrar
# -----------------------------
def f(x):
    return x**2  # función simple para ver el método claramente

# -----------------------------
# integración por trapecio
# -----------------------------
def trapecio(f, a, b, n):
    """
    Aproxima la integral de f en [a,b]
    usando la regla del trapecio compuesta
    """

    h = (b - a) / n  # tamaño del paso (dx)
    x = np.linspace(a, b, n + 1)  # puntos del intervalo

    # suma de extremos + puntos interiores
    suma = f(x[0]) + f(x[-1]) + 2 * np.sum(f(x[1:-1]))

    # fórmula del trapecio
    return (h / 2) * suma


# -----------------------------
# uso del método
# -----------------------------
a, b = 0, 2
n = 1000  # más n → más precisión

resultado = trapecio(f, a, b, n)

print("Resultado por trapecio:", resultado)
print("Valor exacto:", 8/3)
print("Error:", abs(resultado - 8/3))