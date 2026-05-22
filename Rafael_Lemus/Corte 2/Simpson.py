import numpy as np
import matplotlib.pyplot as plt

# Función a integrar
def f(x):
    return np.exp(-x**2)

# Regla de Simpson
def simpson(a, b, n):
    if n % 2 != 0:
        raise ValueError("n debe ser par para la regla de Simpson")

    h = (b - a) / n
    suma = f(a) + f(b)

    for i in range(1, n):
        x = a + i*h

        if i % 2 == 0:
            suma += 2 * f(x)
        else:
            suma += 4 * f(x)

    integral = (h / 3) * suma
    return integral

# Datos
a = 0
b = 2
n = 8   # debe ser par

# Resultado numérico
resultado = simpson(a, b, n)

print("Integral aproximada:", resultado)

# -----------------------------
# Gráfica de Simpson
# -----------------------------
x = np.linspace(a, b, 1000)
y = f(x)

plt.figure(figsize=(9,5))
plt.plot(x, y, label=r'$f(x)=e^{-x^2}$')

# Nodos de Simpson
x_nodes = np.linspace(a, b, n + 1)
y_nodes = f(x_nodes)

# Dibujar aproximaciones parabólicas
for i in range(0, n, 2):
    x0 = x_nodes[i]
    x1 = x_nodes[i+1]
    x2 = x_nodes[i+2]

    y0 = y_nodes[i]
    y1 = y_nodes[i+1]
    y2 = y_nodes[i+2]

    # Ajuste cuadrático
    coef = np.polyfit([x0, x1, x2], [y0, y1, y2], 2)
    p = np.poly1d(coef)

    xs = np.linspace(x0, x2, 200)

    plt.plot(xs, p(xs))
    plt.fill_between(xs, p(xs), alpha=0.3)

# Puntos usados
plt.plot(x_nodes, y_nodes, 'o')

plt.title('Regla de Simpson')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()

plt.show()