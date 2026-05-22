# ----------------------------------------------------------
# INTEGRACIÓN DE ROMBERG
# ----------------------------------------------------------
# Romberg mejora la regla del trapecio.
# Usa varias aproximaciones.
# ----------------------------------------------------------

def f(x):

    return x**2


a = 0
b = 2

# Primer trapecio
n1 = 1
h1 = (b - a) / n1

T1 = (h1 / 2) * (f(a) + f(b))

# Segundo trapecio
n2 = 2
h2 = (b - a) / n2

T2 = (h2 / 2) * (f(a) + 2 * f(a + h2) + f(b))

# Fórmula de Romberg
R = (4 * T2 - T1) / 3

print("Resultado de Romberg:", R)