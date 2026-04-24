import numpy as np
import matplotlib.pyplot as plt

# Parámetros
C = 2.0        # aceleración constante
t_max = 10.0   # tiempo máximo
n = 100        # número de puntos

# Vector de tiempo
t = np.linspace(0, t_max, n)

# Funciones
a = C * np.ones_like(t)     # a(t) = C
v = C * t                   # v(t) = C t
x = 0.5 * C * t**2          # x(t) = (1/2) C t^2

# -------------------------
# Gráfica de aceleración
# -------------------------
plt.figure()
plt.plot(t, a)
plt.xlabel('t')
plt.ylabel('a(t)')
plt.title('Aceleración constante')
plt.grid()
plt.savefig('aceleracion_trapecio.png')
plt.close()

# -------------------------
# Gráfica de velocidad
# -------------------------
plt.figure()
plt.plot(t, v)
plt.xlabel('t')
plt.ylabel('v(t)')
plt.title('Velocidad')
plt.grid()
plt.savefig('velocidad_trapecio.png')
plt.close()

# -------------------------
# Gráfica de posición
# -------------------------
plt.figure()
plt.plot(t, x)
plt.xlabel('t')
plt.ylabel('x(t)')
plt.title('Posición')
plt.grid()
plt.savefig('posicion_trapecio.png')
plt.close()