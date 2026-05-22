# ---------------------------------------------------
# INTEGRACIÓN DE ROMBERG
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------

# Definimos la función:
# f(x) = ln(x + 1)

def f(x):
    return np.log(x + 1)


# ---------------------------------------------------
# DATOS DEL PROBLEMA

# Límite inferior de integración
a = 0

# Límite superior de integración
b = 1

# Número de niveles para Romberg
# Entre más niveles, mayor precisión
niveles = 4

# VALOR EXACTO DE LA INTEGRAL


# La integral exacta de:
# ln(x + 1) entre 0 y 1 es:
#
# 2ln(2) - 1

valor_exacto = 2 * np.log(2) - 1


# ---------------------------------------------------
# MATRIZ DE ROMBERG

# Creamos una matriz llena de ceros
# Aquí se guardarán las aproximaciones

R = np.zeros((niveles, niveles))

# ---------------------------------------------------
# PRIMERA COLUMNA
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------

# Este ciclo calcula las aproximaciones

for i in range(niveles):

    # Número de intervalos
    # Va aumentando

    n = 2**i

    # Calculamos el tamaño del paso
    h = (b - a) / n

    # Generamos los puntos del intervalo
    x = np.linspace(a, b, n + 1)

    # Evaluamos la función en esos puntos
    y = f(x)

    # Iniciamos la suma con:
    # primer valor + último valor
    suma = y[0] + y[-1]

    # Sumamos los valores internos
    # multiplicados por 2
    for j in range(1, n):

        suma += 2 * y[j]

    # Fórmula final del trapecio
    R[i, 0] = (h / 2) * suma

# ---------------------------------------------------
# EXTRAPOLACIÓN DE ROMBERG
# ---------------------------------------------------

# Aquí Romberg mejora las aproximaciones
# usando extrapolación matemática

for i in range(1, niveles):

    for j in range(1, i + 1):

        # Fórmula de Romberg
        R[i, j] = R[i, j - 1] + (
            (R[i, j - 1] - R[i - 1, j - 1])
            / (4**j - 1)
        )


# ---------------------------------------------------
# RESULTADO FINAL

resultado_romberg = R[niveles - 1, niveles - 1]

# Calculamos el error absoluto
error = abs(valor_exacto - resultado_romberg)

# MOSTRAR RESULTADOS
print("VALOR EXACTO:")
print(valor_exacto)

print("\nRESULTADO CON ROMBERG:")
print(resultado_romberg)

print("\nERROR:")
print(error)


# ---------------------------------------------------
# GRÁFICA
x_suave = np.linspace(a, b, 200)

# Evaluamos la función
y_suave = f(x_suave)


# ---------------------------------------------------
# FUNCIÓN ORIGINAL
plt.plot(x_suave, y_suave,
         color='blue',
         label='f(x) = ln(x + 1)')


# ---------------------------------------------------
# PUNTOS UTILIZADOS POR ROMBERG

# Dibujamos los puntos utilizados
plt.plot(x, y,
         'ro',
         label='Puntos utilizados')


# ---------------------------------------------------
# ÁREA APROXIMADA
# Rellenamos el área aproximada

plt.fill_between(x, y,
                 color='orange',
                 alpha=0.3)


# ---------------------------------------------------
# PERSONALIZACIÓN DE LA GRÁFICA

# Título
plt.title("Integración de Romberg")
# Nombre eje X
plt.xlabel("x")
# Nombre eje Y
plt.ylabel("f(x)")
# Cuadrícula
plt.grid(True)
plt.legend()
plt.show()