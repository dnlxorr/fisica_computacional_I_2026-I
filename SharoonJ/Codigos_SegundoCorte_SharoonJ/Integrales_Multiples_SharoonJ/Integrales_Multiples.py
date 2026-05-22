# ---------------------------------------------------
# INTEGRACIÓN MÚLTIPLE
# ---------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------
# FUNCIÓN A INTEGRAR
# ---------------------------------------------------
# f(x,y) = x² + y²
def f(x, y):
    return x**2 + y**2


# ---------------------------------------------------
# LÍMITES DE INTEGRACIÓN
# Región:
# 0 <= x <= 1
# 0 <= y <= 1

a, b = 0, 1
c, d = 0, 1


# ---------------------------------------------------
# MÉTODO DE RIEMANN
# ---------------------------------------------------
# Divide la región en pequeños cuadrados
# y suma las áreas.

def riemann(n):

    # Creamos puntos en x y y
    x = np.linspace(a, b, n)
    y = np.linspace(c, d, n)

    # Tamaño de cada división
    dx = (b - a) / (n - 1)
    dy = (d - c) / (n - 1)

    # Variable acumuladora
    suma = 0

    # Recorremos todos los puntos
    for xi in x:
        for yj in y:

            # función × área pequeña
            suma += f(xi, yj) * dx * dy

    return suma


# ---------------------------------------------------
# MÉTODO DEL TRAPECIO
# ---------------------------------------------------
# Usa trapecios para aproximar el área.

def trapecio(n):

    # Creamos puntos
    x = np.linspace(a, b, n)
    y = np.linspace(c, d, n)

    # Creamos la malla
    X, Y = np.meshgrid(x, y)

    # Evaluamos la función
    Z = f(X, Y)

    # Aplicamos el método del trapecio
    return np.trapezoid(np.trapezoid(Z, x), y)


# ---------------------------------------------------
# MÉTODO MONTE CARLO
# ---------------------------------------------------
# Usa puntos aleatorios para aproximar
# la integral.

def montecarlo(N):

    # Generamos puntos aleatorios
    x_rand = np.random.uniform(a, b, N)
    y_rand = np.random.uniform(c, d, N)

    # Evaluamos la función
    valores = f(x_rand, y_rand)

    # Área de la región
    area = (b - a) * (d - c)

    # Promedio × área
    return area * np.mean(valores)


# ---------------------------------------------------
# VALOR EXACTO
valor_exacto = 2/3


# ---------------------------------------------------
# RESULTADOS NUMÉRICOS
riemann_resultado = riemann(50)
trapecio_resultado = trapecio(50)
montecarlo_resultado = montecarlo(10000)

error_riemann = abs(valor_exacto - riemann_resultado)
error_trapecio = abs(valor_exacto - trapecio_resultado)
error_montecarlo = abs(valor_exacto - montecarlo_resultado)


# ---------------------------------------------------
# TERMINAL
print("========================================")
print("        COMPARACIÓN DE MÉTODOS")
print("========================================\n")

print(f"Valor exacto     : {valor_exacto:.6f}\n")

print(f"Riemann          : {riemann_resultado:.6f}")
print(f"Error            : {error_riemann:.6f}\n")

print(f"Trapecio         : {trapecio_resultado:.6f}")
print(f"Error            : {error_trapecio:.6f}\n")

print(f"Monte Carlo      : {montecarlo_resultado:.6f}")
print(f"Error            : {error_montecarlo:.6f}")


# ---------------------------------------------------
# GRÁFICAS
# ---------------------------------------------------
x = np.linspace(a, b, 50)
y = np.linspace(c, d, 50)

# Creamos la malla
X, Y = np.meshgrid(x, y)

Z = f(X, Y)


# ---------------------------------------------------
# FIGURA GENERAL
fig = plt.figure(figsize=(12,8))

fig.suptitle("Comparación Visual de Métodos Numéricos", fontsize=16)


# ---------------------------------------------------
# 1. FUNCIÓN ORIGINAL
ax1 = fig.add_subplot(221, projection='3d')

ax1.plot_surface(X, Y, Z, cmap='viridis')

ax1.set_title("Función Original")
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.set_zlabel("f(x,y)")


# ---------------------------------------------------
# 2. SUMAS DE RIEMANN
ax2 = fig.add_subplot(222, projection='3d')

ax2.plot_surface(X, Y, Z, cmap='plasma')

ax2.set_title("Sumas de Riemann")
ax2.set_xlabel("x")
ax2.set_ylabel("y")
ax2.set_zlabel("f(x,y)")


# ---------------------------------------------------
# 3. MÉTODO DEL TRAPECIO
ax3 = fig.add_subplot(223, projection='3d')

ax3.plot_surface(X, Y, Z, cmap='coolwarm')

ax3.set_title("Método del Trapecio")
ax3.set_xlabel("x")
ax3.set_ylabel("y")
ax3.set_zlabel("f(x,y)")


# ---------------------------------------------------
# 4. MONTE CARLO
ax4 = fig.add_subplot(224, projection='3d')

ax4.plot_surface(X, Y, Z, cmap='spring')

ax4.set_title("Monte Carlo")
ax4.set_xlabel("x")
ax4.set_ylabel("y")
ax4.set_zlabel("f(x,y)")

plt.tight_layout()
plt.show()