import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# DATOS DEL PROBLEMA
# ==================================================

m = 850          # masa del satélite (kg)

# ==================================================
# FUERZAS
# ==================================================

# Fuerza propulsora variable:
# Fp(t) = 1200 e^(-0.15 t) cos(0.4 t)

# Fuerza de arrastre:
# Fr = -45 v

# Segunda ley de Newton:
#
# m dv/dt = Fp(t) - 45v
#
# dv/dt = (Fp(t) - 45v)/m

# ==================================================
# ECUACIÓN DIFERENCIAL
# ==================================================

def dv_dt(t, v):

    Fp = 1200*np.exp(-0.15*t)*np.cos(0.4*t)

    Fr = -45*v

    return (Fp + Fr)/m

# ==================================================
# MÉTODO DE EULER
# ==================================================

def euler(v0, t0, tf, n):

    h = (tf - t0)/n

    t = np.linspace(t0, tf, n+1)

    v = np.zeros(n+1)

    # condición inicial
    v[0] = v0

    # integración numérica
    for i in range(n):

        v[i+1] = v[i] + h*dv_dt(t[i], v[i])

    return t, v

# ==================================================
# CONDICIONES INICIALES
# ==================================================

v0 = 12      # velocidad inicial (m/s)

t0 = 0
tf = 20

n = 200

# ==================================================
# SOLUCIÓN NUMÉRICA
# ==================================================

t, v = euler(v0, t0, tf, n)

# ==================================================
# POSICIÓN
# ==================================================

# integrar velocidad usando trapecio

x = np.zeros(len(t))

for i in range(len(t)-1):

    h = t[i+1] - t[i]

    x[i+1] = x[i] + h*(v[i] + v[i+1])/2

# ==================================================
# RESULTADOS
# ==================================================

print("Velocidad final =", v[-1], "m/s")
print("Posición final =", x[-1], "m")

# ==================================================
# GRÁFICA VELOCIDAD
# ==================================================

plt.figure(figsize=(8,4))

plt.plot(t, v)

plt.title("Velocidad del satélite")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad (m/s)")

plt.grid()

# ==================================================
# GRÁFICA POSICIÓN
# ==================================================

plt.figure(figsize=(8,4))

plt.plot(t, x)

plt.title("Posición del satélite")
plt.xlabel("Tiempo (s)")
plt.ylabel("Posición (m)")

plt.grid()

plt.show()