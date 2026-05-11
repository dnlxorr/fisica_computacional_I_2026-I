import numpy as np
import matplotlib.pyplot as plt

# -------------------------
# Parámetros físicos
# -------------------------
m = 2.0
Fx = 4.0

ax = Fx / m

v0 = 1.0
x0 = 0.0

t0 = 0.0
t = 20.0

n = 100000
tiempos = np.linspace(t0, t, n + 1)
h = tiempos[1] - tiempos[0]


# -------------------------
# Funciones
# -------------------------
def a(t):
    return ax


def v_exact(t):
    return v0 + ax * (t - t0)


def x_exact(t):
    return x0 + v0 * (t - t0) + 0.5 * ax * (t - t0) ** 2


# -------------------------
# ARRAYS
# -------------------------
v_trap = np.zeros(n + 1)
v_simp = np.zeros(n + 1)

x_trap = np.zeros(n + 1)
x_simp = np.zeros(n + 1)

v_trap[0] = v_simp[0] = v0
x_trap[0] = x_simp[0] = x0

# -------------------------
# INTEGRACIÓN ACUMULATIVA
# -------------------------
for i in range(1, n + 1):

    # -------- VELOCIDAD --------

    # Trapecio
    v_trap[i] = v_trap[i - 1] + (h / 2) * (a(tiempos[i - 1]) + a(tiempos[i]))

    # Simpson
    if i == 1:
        v_simp[i] = v_simp[i - 1] + (h / 2) * (a(tiempos[i - 1]) + a(tiempos[i]))
    elif i % 2 == 0:
        v_simp[i] = v_simp[i - 2] + (h / 3) * (a(tiempos[i - 2]) +
                                               4 * a(tiempos[i - 1]) +
                                               a(tiempos[i]))
    else:
        v_simp[i] = v_simp[i - 1] + (h / 2) * (a(tiempos[i - 1]) + a(tiempos[i]))

    # -------- POSICIÓN --------

    # Trapecio
    x_trap[i] = x_trap[i - 1] + (h / 2) * (v_trap[i - 1] + v_trap[i])

    # Simpson
    if i == 1:
        x_simp[i] = x_simp[i - 1] + (h / 2) * (v_simp[i - 1] + v_simp[i])
    elif i % 2 == 0:
        x_simp[i] = x_simp[i - 2] + (h / 3) * (v_simp[i - 2] +
                                               4 * v_simp[i - 1] +
                                               v_simp[i])
    else:
        x_simp[i] = x_simp[i - 1] + (h / 2) * (v_simp[i - 1] + v_simp[i])

# -------------------------
# EXACTAS
# -------------------------
v_ex = v_exact(tiempos)
x_ex = x_exact(tiempos)

# -------------------------
# GRÁFICAS
# -------------------------

# Velocidad
plt.figure()
plt.plot(tiempos, v_ex, label="Exacta")
plt.plot(tiempos, v_trap, label="Trapecio")
plt.plot(tiempos, v_simp, label="Simpson")
plt.legend()
plt.title("Velocidad vs Tiempo")
plt.xlabel("Tiempo")
plt.ylabel("v")
plt.show()

# Posición
plt.figure()
plt.plot(tiempos, x_ex, label="Exacta")
plt.plot(tiempos, x_trap, label="Trapecio")
plt.plot(tiempos, x_simp, label="Simpson")
plt.legend()
plt.title("Posición vs Tiempo")
plt.xlabel("Tiempo")
plt.ylabel("x")
plt.show()

# Error
plt.figure()
plt.plot(tiempos, np.abs(x_trap - x_ex), label="Error Trapecio")
plt.plot(tiempos, np.abs(x_simp - x_ex), label="Error Simpson")
plt.legend()
plt.title("Error")
plt.xlabel("Tiempo")
plt.ylabel("Error")
plt.show()