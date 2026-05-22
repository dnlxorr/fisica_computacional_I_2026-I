# ---------------------------------------------------
# INTEGRALES SOBRE INTERVALOS INFINITOS
# ---------------------------------------------------

import numpy as np

# Importamos Matplotlib
# Sirve para realizar gráficas
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------
# f(x) = 1 / x²
def f(x):
    return 1 / (x**2)


# ---------------------------------------------------
# DATOS DEL PROBLEMA
# ---------------------------------------------------

# Límite inferior
a = 1

# En vez de infinito usamos un valor grande
# para aproximar la integral impropia
b = 100

# Número de intervalos
n = 1000


# ---------------------------------------------------
# VALOR EXACTO
# La integral exacta es:
# ∫(1/x²) dx desde 1 hasta infinito = 1

valor_exacto = 1


# ---------------------------------------------------
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------
# Calculamos el ancho de paso
h = (b - a) / n

# Generamos puntos
x = np.linspace(a, b, n + 1)

# Evaluamos la función
y = f(x)

# Iniciamos suma
suma = y[0] + y[-1]

# Sumamos puntos internos
for i in range(1, n):
    suma += 2 * y[i]

# Aplicamos fórmula del trapecio
integral = (h / 2) * suma


# ---------------------------------------------------
# CÁLCULO DEL ERROR
# Error absoluto
error = abs(valor_exacto - integral)


# ---------------------------------------------------
# MOSTRAR RESULTADOS
print("VALOR EXACTO:")
print(valor_exacto)

print("\nAPROXIMACIÓN NUMÉRICA:")
print(integral)

print("\nERROR:")
print(error)


# ---------------------------------------------------
# GRÁFICA
# Creamos muchos puntos
# para una curva suave
x_suave = np.linspace(a, b, 500)

# Evaluamos la función
y_suave = f(x_suave)


# ---------------------------------------------------
# FUNCIÓN ORIGINAL
# Dibujamos la curva
plt.plot(x_suave, y_suave,
         color='blue',
         label='f(x) = 1/x²')


# ---------------------------------------------------
# ÁREA APROXIMADA
# Rellenamos el área bajo la curva
plt.fill_between(x_suave, y_suave,
                 color='skyblue',
                 alpha=0.4)


# ---------------------------------------------------
# PERSONALIZACIÓN
plt.title("Integral sobre un Intervalo Infinito")

plt.xlabel("x")

plt.ylabel("f(x)")

plt.grid(True)
plt.legend()

plt.show()