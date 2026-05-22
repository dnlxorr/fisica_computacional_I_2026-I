import numpy as np
import matplotlib.pyplot as plt

# Función a integrar
def f(x):
    return np.cos(x)

# Valor exacto de la integral
# Integral de cos(x) entre 0 y pi/2 = 1
valor_exacto = 1

# Regla del trapecio
def trapecio(a, b, n):
    h = (b - a) / n
    suma = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        suma += f(a + i*h)

    return h * suma

# Regla de Simpson
def simpson(a, b, n):
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

# Intervalo
a = 0
b = np.pi / 2

# Diferentes números de pasos
n_values = np.arange(2, 42, 2)

errores_trap = []
errores_simp = []

# Calcular errores
for n in n_values:
    I_trap = trapecio(a, b, n)
    I_simp = simpson(a, b, n)

    error_trap = abs(valor_exacto - I_trap)
    error_simp = abs(valor_exacto - I_simp)

    errores_trap.append(error_trap)
    errores_simp.append(error_simp)

# -----------------------------
# Gráfica de errores
# -----------------------------
plt.figure(figsize=(8,5))

plt.plot(n_values, errores_trap, 'o-', label='Trapecio')
plt.plot(n_values, errores_simp, 's-', label='Simpson')

plt.yscale('log')

plt.title('Errores en integración numérica')
plt.xlabel('Número de subintervalos (n)')
plt.ylabel('Error absoluto')
plt.grid(True)
plt.legend()

plt.show()