import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Función
# -----------------------------
def f(t):
    return t**3

# solución exacta
def exacta(t):
    return t**4 / 4

# -----------------------------
# Trapecio
# -----------------------------
def trapecio_acumulado(f_vals, t):
    n = len(t)
    h = t[1] - t[0]
    res = np.zeros(n)

    for i in range(1, n):
        res[i] = res[i-1] + (h/2)*(f_vals[i] + f_vals[i-1])

    return res

# -----------------------------
# Simpson
# -----------------------------
def simpson_acumulado(f_vals, t):
    n = len(t)
    h = t[1] - t[0]
    res = np.zeros(n)

    for j in range(2, n, 2):
        suma = f_vals[0] + f_vals[j]

        for i in range(1, j):
            if i % 2 == 0:
                suma += 2 * f_vals[i]
            else:
                suma += 4 * f_vals[i]

        res[j] = (h/3) * suma

        if j+1 < n:
            res[j+1] = res[j]

    return res

# -----------------------------
# Intervalo
# -----------------------------
t = np.linspace(0, 5, 50)
f_vals = f(t)

# -----------------------------
# Resultados
# -----------------------------
trap = trapecio_acumulado(f_vals, t)
simp = simpson_acumulado(f_vals, t)
real = exacta(t)

# -----------------------------
# GRÁFICA
# -----------------------------
plt.figure()

plt.plot(t, real, label="Exacta")
plt.plot(t, trap, "--", label="Trapecio")
plt.plot(t, simp, ":", label="Simpson")

plt.title("Comparación de métodos")
plt.xlabel("Tiempo")
plt.ylabel("Valor")
plt.legend()
plt.grid()

plt.show()