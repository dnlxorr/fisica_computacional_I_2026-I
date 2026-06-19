import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# Función original
def f(x):
    return x**3 - 4*x + 1

# Puntos de la función
x = np.linspace(0, 2*np.pi, 10)
y = f(x)

# Spline cúbico
spline = CubicSpline(x, y)

# Puntos para una curva suave
x_suave = np.linspace(0, 2*np.pi, 1000)
y_suave = spline(x_suave)

# Gráfica
plt.figure(figsize=(8,5))
plt.plot(x_suave, f(x_suave), '--', label='Función original')
plt.plot(x_suave, y_suave, label='Spline cúbico')
plt.plot(x, y, 'o', label='Nodos')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Interpolación con Spline Cúbico')
plt.legend()
plt.grid(True)
plt.show()