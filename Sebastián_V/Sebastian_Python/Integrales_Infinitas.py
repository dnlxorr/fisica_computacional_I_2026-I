import numpy as np

# -----------------------------
# función original
# -----------------------------
def f(x):
    return np.exp(-x)

# -----------------------------
# cambio de variable estable
# x = t/(1-t)
# -----------------------------
def g(t):
    x = t / (1 - t)
    derivada = 1 / (1 - t)**2
    return f(x) * derivada

# -----------------------------
# integración por trapecio
# con corte numérico en 1 - eps
# -----------------------------
def trapecio(f, a, b, n=2000):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)

    return (h / 2) * (
        f(x[0]) + f(x[-1]) + 2 * np.sum(f(x[1:-1]))
    )

# -----------------------------
# evitamos el punto problemático t = 1
# -----------------------------
eps = 1e-10  # evita división por cero
resultado = trapecio(g, 0, 1 - eps, n=3000)

print("Integral transformada:", resultado)