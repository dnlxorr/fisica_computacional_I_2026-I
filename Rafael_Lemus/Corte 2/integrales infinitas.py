import numpy as np
import matplotlib.pyplot as plt

# Función a integrar
def f(x):
    return np.exp(-x)

# Regla de Simpson
def simpson(f, a, b, n):

    if n % 2 != 0:
        raise ValueError("n debe ser par")

    h = (b - a) / n

    suma = f(a) + f(b)

    for i in range(1, n):

        x = a + i*h

        if i % 2 == 0:
            suma += 2 * f(x)
        else:
            suma += 4 * f(x)

    return (h / 3) * suma

# ==========================================
# MÉTODO 1: TRUNCAMIENTO
# ==========================================

# Aproximar:
# integral de 0 a infinito
# usando un límite grande

L = 10

n = 100

integral_truncada = simpson(f, 0, L, n)

# ==========================================
# MÉTODO 2: CAMBIO DE VARIABLE
# ==========================================

# Transformación:
# x = t/(1-t)

def g(t):

    x = t / (1 - t)

    dx_dt = 1 / (1 - t)**2

    return f(x) * dx_dt

# Integrar en t entre 0 y 1
integral_cambio = simpson(g, 0, 0.999, n)

# ==========================================
# VALOR EXACTO
# ==========================================

valor_exacto = 1

# Errores
error_trunc = abs(valor_exacto - integral_truncada)
error_cambio = abs(valor_exacto - integral_cambio)

# ==========================================
# RESULTADOS
# ==========================================

print("========== TRUNCAMIENTO ==========")
print("Integral aproximada:", integral_truncada)
print("Error:", error_trunc)

print()

print("====== CAMBIO DE VARIABLE ======")
print("Integral aproximada:", integral_cambio)
print("Error:", error_cambio)

# ==========================================
# GRÁFICAS
# ==========================================

x = np.linspace(0, 10, 1000)

t = np.linspace(0, 0.999, 1000)

plt.figure(figsize=(8,5))
plt.plot(x, f(x))

plt.title('Función original')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)

plt.figure(figsize=(8,5))
plt.plot(t, g(t))

plt.title('Función transformada')
plt.xlabel('t')
plt.ylabel('g(t)')
plt.grid(True)

plt.show()