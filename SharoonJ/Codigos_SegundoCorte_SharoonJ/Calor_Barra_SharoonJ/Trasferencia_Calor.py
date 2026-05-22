import numpy as np
import matplotlib.pyplot as plt

# =========================================================
# 1. PARÁMETROS FÍSICOS DEL PROBLEMA
# =========================================================

L = 10
# Longitud total de la barra metálica

alpha = 0.1
# Difusividad térmica
# Representa qué tan rápido se propaga el calor dentro del material.

T_total = 20
# Tiempo total de simulación

# 2. DISCRETIZACIÓN DEL PROBLEMA
nx = 50
# Número de puntos espaciales en los que se divide la barra

nt = 500
# Número total de pasos de tiempo

dx = L / (nx - 1)
# Distancia entre puntos consecutivos


dt = T_total / nt
# Tamaño del paso temporal


# ---------------------------------------------------
# 3. PARÁMETRO NUMÉRICO
r = alpha * dt / dx ** 2

# Este parámetro controla:
# → La estabilidad numérica
# → La velocidad de propagación del calor


#------------------------------------------------------------
# 4. POSICIÓN EN LA BARRA
x = np.linspace(0, L, nx)
# Se genera un arreglo con todas las posiciones desde x = 0 hasta x = L


#-----------------------------------------------------------
# 5. CONDICIÓN INICIAL

T = np.zeros(nx)
# Inicialmente toda la barra tiene temperatura igual a cero.

# 6. FUENTE DE CALOR
T[nx // 2] = 100

# Se coloca una temperatura alta
# exactamente en el centro de la barra.


#----------------------------------------------------------
# 7. CONFIGURACIÓN DE LA GRÁFICA

plt.figure(figsize=(12, 6))
# Tamaño de la figura


# ---------------------------------------------------
# 8. EVOLUCIÓN TEMPORAL DEL CALOR

for n in range(nt):

    # CREAR COPIA TEMPORAL

    T_new = T.copy()

    # Esta copia almacenará
    # las nuevas temperaturas.

    # ECUACIÓN DE DIFERENCIAS FINITAS

    # T_new[i] = T[i] + r * (T[i+1] - 2T[i] + T[i-1])

    # → T[i]     = temperatura actual
    # → T[i+1]   = vecino derecho
    # → T[i-1]   = vecino izquierdo

    for i in range(1, nx - 1):
        T_new[i] = T[i] + r * (
                T[i + 1]
                - 2 * T[i]
                + T[i - 1]
        )

    # ACTUALIZAR TEMPERATURAS

    T = T_new.copy()

    # Las temperaturas nuevas
    # reemplazan las anteriores.

    # MOSTRAR ALGUNOS INSTANTES

    if n % 100 == 0:
        tiempo = n * dt

        # Graficar evolución térmica
        plt.plot(
            x,
            T,
            linewidth=2,
            label=f't = {tiempo:.1f}'
        )


# ---------------------------------------------------
# 9. GRÁFICA

plt.title(
    'Transferencia de Calor en una Barra',
    fontsize=18
)

plt.xlabel(
    'Posición en la barra',
    fontsize=12
)

plt.ylabel(
    'Temperatura',
    fontsize=12
)

plt.legend()
# Cuadrícula
plt.grid(True)

plt.show()
