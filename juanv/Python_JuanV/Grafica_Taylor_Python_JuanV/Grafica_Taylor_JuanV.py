import math
import matplotlib.pyplot as plt
import numpy as np

# Función original
def f(x):
    return math.sin(x)

# Taylor 3 términos
def taylor_3(x):
    return x - (x**3)/math.factorial(3) + (x**5)/math.factorial(5)

# Taylor 6 términos
def taylor_6(x):
    return (x
            - (x**3)/math.factorial(3)
            + (x**5)/math.factorial(5)
            - (x**7)/math.factorial(7)
            + (x**9)/math.factorial(9)
            - (x**11)/math.factorial(11))

# Rango de valores
x_vals = np.linspace(-3, 3, 100)

# Evaluaciones
y_real = [f(x) for x in x_vals]
y_t3 = [taylor_3(x) for x in x_vals]
y_t6 = [taylor_6(x) for x in x_vals]

# Error cuadrático medio
def mse(real, aprox):
    return sum((r - a)**2 for r, a in zip(real, aprox)) / len(real)

error_t3 = mse(y_real, y_t3)
error_t6 = mse(y_real, y_t6)

print("Error cuadrático medio (3 términos):", error_t3)
print("Error cuadrático medio (6 términos):", error_t6)

# Gráfica
plt.plot(x_vals, y_real, label="sin(x)")
plt.plot(x_vals, y_t3, label="Taylor 3 términos")
plt.plot(x_vals, y_t6, label="Taylor 6 términos")

plt.legend()
plt.title("Aproximación de Taylor de sin(x)")
plt.grid()

plt.show()