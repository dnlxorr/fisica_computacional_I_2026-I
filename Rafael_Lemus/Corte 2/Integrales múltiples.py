import numpy as np
import matplotlib.pyplot as plt

# Función de dos variables
def f(x, y):
    return np.exp(-(x**2 + y**2))

# Integración doble usando la regla del trapecio
def trapecio_doble(f, ax, bx, ay, by, nx, ny):

    hx = (bx - ax) / nx
    hy = (by - ay) / ny

    suma = 0

    for i in range(nx + 1):

        x = ax + i * hx

        for j in range(ny + 1):

            y = ay + j * hy

            # Peso en x
            if i == 0 or i == nx:
                px = 0.5
            else:
                px = 1

            # Peso en y
            if j == 0 or j == ny:
                py = 0.5
            else:
                py = 1

            suma += px * py * f(x, y)

    return hx * hy * suma

# Intervalos de integración
ax = -1
bx = 1

ay = -1
by = 1

# Número de subdivisiones
nx = 50
ny = 50

# Aproximación numérica
resultado = trapecio_doble(f, ax, bx, ay, by, nx, ny)

# Mostrar resultado
print("Integral doble aproximada:")
print(resultado)

# -----------------------------------
# Gráfica de la superficie
# -----------------------------------

x = np.linspace(ax, bx, 100)
y = np.linspace(ay, by, 100)

X, Y = np.meshgrid(x, y)

Z = f(X, Y)

fig = plt.figure(figsize=(9,6))

ax3d = fig.add_subplot(111, projection='3d')

ax3d.plot_surface(X, Y, Z)

ax3d.set_title('Superficie f(x,y)')
ax3d.set_xlabel('x')
ax3d.set_ylabel('y')
ax3d.set_zlabel('f(x,y)')

plt.show()