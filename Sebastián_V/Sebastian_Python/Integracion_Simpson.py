import numpy as np

# -----------------------------
# función a integrar
# -----------------------------
def f(x):
    return x**2

# -----------------------------
# integración por Simpson
# -----------------------------
def simpson(f, a, b, n):
    """
    Aproxima la integral usando la regla de Simpson compuesta
    IMPORTANTE: n debe ser par
    """

    if n % 2 != 0:
        raise ValueError("n debe ser par para Simpson")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)

    # puntos pares e impares
    suma_impares = np.sum(f(x[1:n:2]))  # multiplicados por 4
    suma_pares = np.sum(f(x[2:n-1:2]))  # multiplicados por 2

    # fórmula de Simpson
    integral = (h / 3) * (f(x[0]) + f(x[-1]) + 4 * suma_impares + 2 * suma_pares)

    return integral


# -----------------------------
# uso del método
# -----------------------------
a, b = 0, 2
n = 1000  # debe ser par

resultado = simpson(f, a, b, n)

print("Resultado por Simpson:", resultado)
print("Valor exacto:", 8/3)
print("Error:", abs(resultado - 8/3))