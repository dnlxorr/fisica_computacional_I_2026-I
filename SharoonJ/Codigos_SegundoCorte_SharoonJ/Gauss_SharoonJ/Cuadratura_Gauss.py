import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# f(x) = x² cos(x) + 2
def f(x):
    return x**2 * np.cos(x) + 2


# ---------------------------------------------------
# INTERVALO DE INTEGRACIÓN
# La integral va
a = -5
b = 5


# ---------------------------------------------------
# VALOR EXACTO (REFERENCIA)
# quad() usa métodos adaptativos muy precisos.
# Se usa para comparar: que tan bueno es algo
# - Qué tan bueno es Simpson
# - Qué tan bueno es Gauss
# I_exacta → valor aproximado de la integral
I_exacta, _ = quad(f, a, b)


# =========================================================
# MÉTODO DE SIMPSON
# =========================================================

# h  → tamaño del paso
# x0, x1, x2, ... xn → puntos igualmente espaciados
# n PAR


# ---------------------------------------------------------
# NÚMERO DE SUBINTERVALOS
n_simpson = 24


# ---------------------------------------------------------
# TAMAÑO DEL PASO
h = (b - a) / n_simpson


# ---------------------------------------------------------
# PUNTOS EQUIDISTANTES
x_simpson = np.linspace(a, b, n_simpson + 1)


# ---------------------------------------------------------
# EVALUACIÓN DE LA FUNCIÓN
# Calculamos:
# f(x0), f(x1), f(x2), ...
y_simpson = f(x_simpson)


# ---------------------------------------------------
# APLICACIÓN MANUAL DE LA FÓRMULA DE SIMPSON
suma = y_simpson[0] + y_simpson[-1]


# ---------------------------------------------------------
# SUMATORIA CENTRAL
# ---------------------------------------------------------
for i in range(1, n_simpson):

    # -----------------------------------------------------
    # SI EL ÍNDICE ES IMPAR
    # Se multiplica por 4

    if i % 2 != 0:
        suma += 4 * y_simpson[i]

    # -----------------------------------------------------
    # SI EL ÍNDICE ES PAR
    # Se multiplica por 2
    else:
        suma += 2 * y_simpson[i]


# ---------------------------------------------------------
# RESULTADO FINAL DE SIMPSON
# ---------------------------------------------------------
I_simpson = (h / 3) * suma


# =========================================================
# CUADRATURA DE GAUSS
# =========================================================
# para obtener mucha precisión con pocos puntos.
# wi → pesos
# xi → nodos especiales
# de [-1, 1] transformacion del intervalo a [a,b]


# ---------------------------------------------------------
# NÚMERO DE NODOS
n_gauss = 8


# ---------------------------------------------------------
# GENERACIÓN DE NODOS Y PESOS
# leggauss(n):
# devuelve
# t → nodos
# w → pesos
t, w = leggauss(n_gauss)


# ---------------------------------------------------
# CAMBIO DE VARIABLE
# Los nodos están en:
# [-1,1]
# pero necesitamos:
# [a,b]
# Transformación:
# x = ((b-a)/2)t + ((a+b)/2)
x_gauss = ((b - a) / 2) * t + ((a + b) / 2)


# ---------------------------------------------------------
# EVALUACIÓN DE LA FUNCIÓN
y_gauss = f(x_gauss)


# ---------------------------------------------------
# APLICACIÓN DE LA FÓRMULA DE GAUSS
# suma todos los términos:
I_gauss = ((b - a) / 2) * np.sum(w * y_gauss)


# ---------------------------------------------------
# COMPARACIÓN NUMÉRICA
error_simpson = abs(I_exacta - I_simpson)
error_gauss = abs(I_exacta - I_gauss)


# ---------------------------------------------------
# IMPRESIÓN DE RESULTADOS
print("\n================================================")
print("        COMPARACIÓN DE MÉTODOS NUMÉRICOS")
print("================================================\n")
print(f"Valor exacto                = {I_exacta:.10f}")


# ---------------------------------------------------------
# RESULTADOS DE SIMPSON
print("\n--------------- SIMPSON ----------------")
print(f"Integral aproximada         = {I_simpson:.10f}")
print(f"Error absoluto              = {error_simpson:.10e}")


# ---------------------------------------------------------
# RESULTADOS DE GAUSS
print("\n----------- CUADRATURA DE GAUSS ----------")
print(f"Integral aproximada         = {I_gauss:.10f}")
print(f"Error absoluto              = {error_gauss:.10e}")
print("\n================================================")


# ---------------------------------------------------------
# MUCHOS PUNTOS PARA LA CURVA SUAVE
# 1000 puntos hacen que la gráfica se vea continua
x = np.linspace(a, b, 1000)

y = f(x)


# ---------------------------------------------------------
# TAMAÑO DE LA FIGURA
plt.figure(figsize=(14,7))


# ---------------------------------------------------
# FUNCIÓN ORIGINAL
plt.plot(
    x,
    y,
    linewidth=3,
    label='Función original'
)


# ---------------------------------------------------
# PUNTOS DE SIMPSON

# 'o--'
# o  → círculos
# -- → línea punteada
plt.plot(
    x_simpson,
    y_simpson,
    'o--',
    linewidth=2,
    markersize=5,
    label='Simpson'
)


# ---------------------------------------------------
# NODOS DE GAUSS

# 's-'
# s → cuadrados
# - → línea continua
plt.plot(
    x_gauss,
    y_gauss,
    's-',
    linewidth=2,
    markersize=7,
    label='Gauss'
)


# ---------------------------------------------------
# ÁREA BAJO LA CURVA
plt.fill_between(
    x,
    y,
    alpha=0.15
)


# ---------------------------------------------------
#GRÁFICA
plt.title('Comparación: Simpson vs Cuadratura de Gauss')

plt.xlabel('x')

plt.ylabel('f(x)')

plt.grid(True)

plt.legend()
plt.show()