import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# DIFRACCIÓN E INTERFERENCIA DE LUZ
# Física Computacional
# =========================================================

# =========================================================
# TEMAS DEL CURSO UTILIZADOS
# =========================================================

# ✔ Series de Taylor
# ✔ Integración numérica (Regla de Simpson)
# ✔ Error de truncamiento
# ✔ Error de redondeo
# ✔ Discretización
# ✔ Gráficas 2D
# ✔ Funciones
# ✔ Ciclos for

# =========================================================
# 1. PARÁMETROS FÍSICOS
# =========================================================

A = 1                 # Amplitud
k = 8                 # Número de onda

# Dominio espacial
x = np.linspace(-10, 10, 1000)

# =========================================================
# 2. SERIE DE TAYLOR
# Aproximación para sin(x)
# =========================================================

def taylor_sin(z):

    return z - (z**3)/6 + (z**5)/120

# =========================================================
# 3. ONDAS INTERFERENTES
# =========================================================

# Onda 1
onda1 = A * taylor_sin(k*x)

# Onda 2
onda2 = A * taylor_sin(k*x + np.pi/2)

# Superposición
interferencia = onda1 + onda2

# =========================================================
# 4. ERROR DE REDONDEO
# =========================================================

# Redondeo computacional
interferencia_redondeada = np.round(interferencia, 4)

# =========================================================
# 5. REGLA DE SIMPSON
# =========================================================

def simpson(x, y):

    n = len(x)

    # Simpson necesita número impar
    if n % 2 == 0:
        n -= 1
        x = x[:n]
        y = y[:n]

    h = (x[-1] - x[0]) / (n - 1)

    suma = y[0] + y[-1]

    for i in range(1, n - 1):

        if i % 2 == 0:
            suma += 2 * y[i]

        else:
            suma += 4 * y[i]

    return (h / 3) * suma

# =========================================================
# 6. INTEGRACIÓN NUMÉRICA
# =========================================================

energia = simpson(x, interferencia_redondeada**2)

print("===================================")
print("INTERFERENCIA Y DIFRACCIÓN")
print("===================================")

print(f"Energía aproximada: {energia:.4f}")

# =========================================================
# 7. GRÁFICAS
# =========================================================

plt.figure(figsize=(12,6))

# Onda 1
plt.plot(x, onda1, label='Onda 1')

# Onda 2
plt.plot(x, onda2, label='Onda 2')

# Interferencia
plt.plot(x, interferencia_redondeada,
         linewidth=2,
         label='Interferencia')

# =========================================================
# CONFIGURACIÓN
# =========================================================

plt.title('Interferencia y Difracción de Luz')

plt.xlabel('Posición')
plt.ylabel('Amplitud')

plt.legend()
plt.grid(True)

plt.show()