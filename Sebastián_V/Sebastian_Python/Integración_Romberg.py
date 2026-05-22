import numpy as np

# -----------------------------
# Función a integrar
# -----------------------------
f = lambda x: np.sin(x)

# -----------------------------
# Regla del trapecio compuesta
# -----------------------------
def trapecio(f, a, b, n):
    """
    Aproxima la integral de f en [a,b]
    usando n subintervalos (trapecios).
    """
    h = (b - a) / n  # tamaño del paso
    x = np.linspace(a, b, n + 1)  # puntos de evaluación

    # fórmula del trapecio compuesto:
    # extremos pesan 1, interior pesa 2
    integral = f(x[0]) + f(x[-1]) + 2 * np.sum(f(x[1:-1]))
    return (h / 2) * integral


# -----------------------------
# Tabla de Romberg
# -----------------------------
def romberg(f, a, b, max_iter=6):
    """
    Construye la tabla de Romberg:
    mejora sucesiva del trapecio + extrapolación de Richardson
    """

    R = np.zeros((max_iter, max_iter))

    # Primera columna: trapecio con refinamiento progresivo
    for i in range(max_iter):
        n = 2**i  # duplicamos particiones cada vez
        R[i, 0] = trapecio(f, a, b, n)

    # Extrapolación de Richardson
    for j in range(1, max_iter):
        for i in range(j, max_iter):
            R[i, j] = (4**j * R[i, j-1] - R[i-1, j-1]) / (4**j - 1)

    return R


# -----------------------------
# Ejecutar el método
# -----------------------------
tabla = romberg(f, 0, np.pi, max_iter=6)

# Resultado final (mejor aproximación)
resultado = tabla[-1, -1]

print("Tabla de Romberg:\n")
print(np.round(tabla, 8))

print("\nAproximación final:")
print(resultado)