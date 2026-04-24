import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Método del Trapecio acumulado
# -----------------------------
def trapecio_acumulado(f, t):
    n = len(t)
    h = t[1] - t[0]
    resultado = np.zeros(n)

    for i in range(1, n):
        resultado[i] = resultado[i-1] + (h/2)*(f[i] + f[i-1])

    return resultado


# -----------------------------
# Datos del problema
# -----------------------------
m = 2
Fx, Fy = 6, 8

# condiciones iniciales
v0x, v0y = 5, 3

t0 = 0
tf = 20
n = 100

t = np.linspace(t0, tf, n)

# -----------------------------
# Aceleración (constante)
# -----------------------------
ax = np.full(n, Fx/m)
ay = np.full(n, Fy/m)

# -----------------------------
# Integración: aceleración → velocidad
# -----------------------------
vx = trapecio_acumulado(ax, t) + v0x
vy = trapecio_acumulado(ay, t) + v0y

# -----------------------------
# Integración: velocidad → posición
# -----------------------------
x = trapecio_acumulado(vx, t)
y = trapecio_acumulado(vy, t)

# -----------------------------
# Resultados
# -----------------------------
print("Posición final (Trapecio):")
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