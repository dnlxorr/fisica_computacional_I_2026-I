import math
import numpy as np
import matplotlib.pyplot as plt

# puntos continuos entre -3 y 3
x_valores = np.linspace(-3, 3, 200)

cos_real = []
cos_taylor = []
errores_cuadrados = []

for x in x_valores:

    # coseno real
    real = math.cos(x)
    cos_real.append(real)

    # serie de Taylor hasta n = 6
    taylor = 0
    for n in range(7):
        termino = ((-1)**n) * (x**(2*n)) / math.factorial(2*n)
        taylor += termino

    cos_taylor.append(taylor)

    # error cuadrado
    error = real - taylor
    errores_cuadrados.append(error**2)

# error cuadrático medio
ecm = sum(errores_cuadrados) / len(x_valores)

print("Error cuadrático medio:", ecm)

# gráfica
plt.plot(x_valores, cos_real, label="cos(x) real")
plt.plot(x_valores, cos_taylor, label="Taylor n=6")
plt.xlabel("x")
plt.ylabel("Valor")
plt.title("Comparación cos(x) vs Serie de Taylor (n=6)")
plt.legend()
plt.grid(True)

plt.show()