import numpy as np

# Parámetros físicos
g = 9.81
L = 1.0
theta0 = np.pi / 3


# Integrando con cambio de variable
def integrando_t(t):
    theta = theta0 - t ** 2
    dtheta_dt = -2 * t

    # valor absoluto para evitar problemas numéricos
    return abs(dtheta_dt) / np.sqrt(2 * (np.cos(theta) - np.cos(theta0)))


# Regla del trapecio (sin problemas ahora)
def trapecio(f, a, b, n):
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


# Cálculo del período
def periodo(n):
    integral = trapecio(integrando_t, 1, np.sqrt(theta0), n)
    return 4 * np.sqrt(L / g) * integral


# --- Cálculos ---
n = 100

T_h = periodo(n)
T_h2 = periodo(2 * n)

# Richardson (p = 2)
T_richardson = (4 * T_h2 - T_h) / 3

# --- Resultados ---
print("Trapecio (n):", T_h)
print("Trapecio (2n):", T_h2)
print("Richardson:", T_richardson)