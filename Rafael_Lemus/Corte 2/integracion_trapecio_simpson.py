import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# DATOS FÍSICOS
# ==================================================

m = 1       # masa (kg)
Fx = 2      # fuerza constante en x (N)
v0y = 10    # velocidad inicial en y (m/s)

# ==================================================
# ACELERACIÓN
# ==================================================

# Segunda ley de Newton:
# a = F/m

ax = Fx / m

# En y no hay fuerza
ay = 0

# ==================================================
# POSICIÓN
# ==================================================

# Movimiento en x:
# x(t) = 1/2 a t²

def x(t):
    return 0.5 * ax * t**2

# Movimiento en y:
# y(t) = v0 t

def y(t):
    return v0y * t

# ==================================================
# VELOCIDAD
# ==================================================

# velocidad total:
# v = sqrt(vx² + vy²)

def v(t):

    vx = ax * t
    vy = v0y

    return np.sqrt(vx**2 + vy**2)

# ==================================================
# REGLA DEL TRAPECIO
# ==================================================

def trapecio(a, b, n):

    h = (b - a)/n

    t = np.linspace(a, b, n+1)

    return h * (
        0.5*v(t[0]) +
        np.sum(v(t[1:-1])) +
        0.5*v(t[-1])
    )

# ==================================================
# REGLA DE SIMPSON
# ==================================================

def simpson(a, b, n):

    if n % 2 != 0:
        n += 1

    h = (b - a)/n

    t = np.linspace(a, b, n+1)

    return (h/3) * (
        v(t[0]) +
        4*np.sum(v(t[1:-1:2])) +
        2*np.sum(v(t[2:-2:2])) +
        v(t[-1])
    )

# ==================================================
# INTERVALO
# ==================================================

a = 0
b = 10

n = 100

# ==================================================
# INTEGRACIÓN
# ==================================================

dist_trap = trapecio(a, b, n)
dist_simp = simpson(a, b, n)

# ==================================================
# RESULTADOS
# ==================================================

print("===== RESULTADOS =====\n")

print("Aceleración en x =", ax)

print()

print("Distancia (Trapecio) =", dist_trap)
print("Distancia (Simpson) =", dist_simp)

# ==================================================
# GRÁFICA VELOCIDAD VS TIEMPO
# ==================================================

t = np.linspace(a, b, 500)

plt.figure(figsize=(8,4))

plt.plot(t, v(t))

plt.fill_between(t, v(t), alpha=0.3)

plt.title("Velocidad vs Tiempo")
plt.xlabel("t (s)")
plt.ylabel("v(t) (m/s)")

plt.grid()

# ==================================================
# GRÁFICA DE LA TRAYECTORIA
# ==================================================

plt.figure(figsize=(6,6))

plt.plot(x(t), y(t))

plt.scatter(x(t[0]), y(t[0]), label="Inicio")
plt.scatter(x(t[-1]), y(t[-1]), label="Final")

plt.title("Trayectoria de la partícula")
plt.xlabel("x (m)")
plt.ylabel("y (m)")

plt.grid()
plt.legend()

plt.show()