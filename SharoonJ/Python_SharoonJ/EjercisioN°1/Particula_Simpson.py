import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Método de Simpson acumulado
# -----------------------------
def simpson_acumulado(f, t):
    n = len(t)
    h = t[1] - t[0]
    resultado = np.zeros(n)

    for j in range(2, n, 2):
        suma = f[0] + f[j]

        for i in range(1, j):
            if i % 2 == 0:
                suma += 2 * f[i]
            else:
                suma += 4 * f[i]

        resultado[j] = (h/3) * suma

        # para puntos impares (interpolación simple)
        if j+1 < n:
            resultado[j+1] = resultado[j]

    return resultado

# -----------------------------
# Datos del problema3
66666
# -----------------------------
m = 2
Fx, Fy = 6, 8

# condiciones iniciales
v0x, v0y = 5, 3

t0 = 0
tf = 20
n = 100  # debe ser par

t = np.linspace(t0, tf, n)

# -----------------------------
# Aceleraciones (constantes)
# -----------------------------
ax = np.full(n, Fx/m)
ay = np.full(n, Fy/m)

# -----------------------------
# Integrar aceleración → velocidad
# -----------------------------
vx = simpson_acumulado(ax, t) + v0x
vy = simpson_acumulado(ay, t) + v0y

# -----------------------------
# Integrar velocidad → posición
# -----------------------------
x = simpson_acumulado(vx, t)
y = simpson_acumulado(vy, t)

# -----------------------------
# Resultados finales
# -----------------------------
print("Posición final:")
print("x =", x[-1])
print("y =", y[-1])

# -----------------------------
# GRÁFICAS
# -----------------------------

# Aceleración
plt.figure()
plt.plot(t, ax, label="ax")
plt.plot(t, ay, label="ay")
plt.xlabel("Tiempo (s)")
plt.ylabel("Aceleración")
plt.title("Aceleración vs Tiempo")
plt.legend()
plt.grid()

# Velocidad
plt.figure()
plt.plot(t, vx, label="vx")
plt.plot(t, vy, label="vy")
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad")
plt.title("Velocidad vs Tiempo")
plt.legend()
plt.grid()

# Posición vs tiempo
plt.figure()
plt.plot(t, x, label="x(t)")
plt.plot(t, y, label="y(t)")
plt.xlabel("Tiempo (s)")
plt.ylabel("Posición")
plt.title("Posición vs Tiempo")
plt.legend()
plt.grid()

# Trayectoria
plt.figure()
plt.plot(x, y)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trayectoria de la partícula")
plt.grid()

plt.show()