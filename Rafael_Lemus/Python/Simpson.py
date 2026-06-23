import numpy as np
import matplotlib.pyplot as plt

# Parámetros
C = 2.0  # aceleración constante
t_max = 10.0  # tiempo máximo
n = 100  # número de subintervalos (DEBE SER PAR)

if n % 2 != 0:
    raise ValueError("n debe ser par para Simpson")

# Vector de tiempo
t = np.linspace(0, t_max, n + 1)
h = t[1] - t[0]

# Función aceleración
a = C * np.ones_like(t)


# -------------------------
# Función Simpson
# -------------------------
def simpson(y, h):
    n = len(y) - 1
    S = y[0] + y[-1]

    for i in range(1, n):
        if i % 2 == 0:
            S += 2 * y[i]
        else:
            S += 4 * y[i]

    return (h / 3) * S


# -------------------------
# Calcular velocidad con Simpson acumulado
# -------------------------
v = np.zeros_like(t)

for i in range(2, len(t), 2):
    v[i] = simpson(a[:i + 1], h)
    v[i - 1] = v[i]  # aproximación para puntos intermedios

# -------------------------
# Calcular posición con Simpson acumulado
# -------------------------
x = np.zeros_like(t)

for i in range(2, len(t), 2):
    x[i] = simpson(v[:i + 1], h)
    x[i - 1] = x[i]

# -------------------------
# Gráfica de aceleración
# -------------------------
plt.figure()
plt.plot(t, a)
plt.xlabel('t')
plt.ylabel('a(t)')
plt.title('Aceleración (Simpson)')
plt.grid()
plt.savefig('aceleracion_simpson.png')
plt.close()

# -------------------------
# Gráfica de velocidad
# -------------------------
plt.figure()
plt.plot(t, v)
plt.xlabel('t')
plt.ylabel('v(t)')
plt.title('Velocidad (Simpson)')
plt.grid()
plt.savefig('velocidad_simpson.png')
plt.close()

# -------------------------
# Gráfica de posición
# -------------------------
plt.figure()
plt.plot(t, x)
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Posición (Simpson)')
plt.grid()
plt.savefig('posicion_simpson.png')
plt.close()