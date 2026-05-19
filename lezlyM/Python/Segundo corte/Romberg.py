import numpy as np


def metodo_trapecio_puntos(f, a, b, n):
    """Función auxiliar para calcular el trapecio compuesto estándar."""
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += 2 * f(a + i * h)
    return (h / 2) * suma


def integracion_romberg(f, a, b, filas):
    """
    Calcula la integral aproximada de f(x) desde 'a' hasta 'b'
    construyendo una tabla de Romberg de tamaño (filas x filas).
    """
    # 1. Crear una matriz cuadrada vacía llena de ceros
    R = np.zeros((filas, filas))

    # 2. Llenar la primera columna con el método del trapecio compuesto
    # Cada fila duplica el número de subintervalos: 1, 2, 4, 8, 16... (2^k)
    for k in range(filas):
        n = 2 ** k
        R[k, 0] = metodo_trapecio_puntos(f, a, b, n)

    # 3. Llenar las columnas restantes usando la extrapolación de Richardson
    for j in range(1, filas):
        for k in range(j, filas):
            # Esta es la fórmula matemática central de Romberg
            factor = 4 ** j
            R[k, j] = (factor * R[k, j - 1] - R[k - 1, j - 1]) / (factor - 1)

    # Mostrar la tabla en pantalla para entender el proceso visualmente
    print("--- Tabla de Romberg ---")
    for i in range(filas):
        valores_fila = [f"{R[i, j]:.8f}" for j in range(i + 1)]
        print(f"Fila {i}: {valores_fila}")
    print("-" * 24)

    # 4. El valor más preciso siempre está en la esquina inferior derecha
    return R[filas - 1, filas - 1]


# --- Ejemplo de uso ---

# Función a integrar: f(x) = 1 / (1 + x)
def mi_funcion(x):
    return 1 / (1 + x)


limite_inferior = 0  # Punto 'a'
limite_superior = 1  # Punto 'b'
num_filas = 4  # Generará una tabla de 4x4 (máximo 8 intervalos en trapecio)

# Llamada a la función
resultado = integracion_romberg(mi_funcion, limite_inferior, limite_superior, num_filas)

print(f"Resultado final de Romberg: {resultado:.8f}")
# El valor analítico exacto es ln(2) ≈ 0.69314718