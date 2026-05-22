import numpy as np
import matplotlib.pyplot as plt


# Función a integrar
def f(x):
    return np.sin(x)


# Regla del trapecio
def trapecio(a, b, n):
    h = (b - a) / n
    suma = ( f(a) + f(b) )/ 2

    for i in range(1, n):
        suma += f(a + i * h)

    integral = h * suma
    return integral


# Datos
a = 0
b = np.pi
n = 6

# Resultado numérico
resultado = trapecio(a, b, n)

# Valor exacto
exacto = 2

print("Integral aproximada:", resultado)
print("Valor exacto:", exacto)
print("Error absoluto:", abs(exacto - resultado))

# -----------------------------
# Gráfica de la función
# -----------------------------
x = np.linspace(a, b, 1000)
y = f(x)

plt.figure(figsize=(8, 5))
plt.plot(x, y, label='f(x) = sin(x)')

# Puntos de los trapecios
x_trap = np.linspace(a, b, n + 1)
y_trap = f(x_trap)

# Dibujar trapecios
for i in range(n):
    xs = [x_trap[i], x_trap[i], x_trap[i + 1], x_trap[i + 1]]
    ys = [0, y_trap[i], y_trap[i + 1], 0]

    plt.fill(xs, ys, alpha=0.3)

# Dibujar líneas de los trapecios
plt.plot(x_trap, y_trap, 'o-')

plt.title('Regla del Trapecio')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid(True)
plt.legend()

plt.show()