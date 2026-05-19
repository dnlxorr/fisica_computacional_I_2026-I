import math


def metodo_trapecio(f, a, b, n):
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        suma += 2 * f(a + i * h)
    return (h / 2) * suma


def metodo_simpson(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("Para Simpson, 'n' debe ser par.")
    h = (b - a) / n
    suma = f(a) + f(b)
    for i in range(1, n):
        if i % 2 != 0:
            suma += 4 * f(a + i * h)
        else:
            suma += 2 * f(a + i * h)
    return (h / 3) * suma


# --- SCRIPT DE ANÁLISIS DE ERRORES ---

# 1. Definimos la función f(x) = 1/x
def f(x):
    return 1 / x


a = 1  # Límite inferior
b = 2  # Límite superior

# El valor exacto teórico usando la librería matemática de Python
valor_exacto = math.log(2)

print(f"Valor exacto de la integral (ln(2)): {valor_exacto}\n")
print(f"{'Intervalos (n)':<15}{'Error Trapecio':<20}{'Error Simpson':<20}")
print("-" * 55)

# Evaluamos con diferentes cantidades de intervalos para ver cómo cae el error
for n in [4, 10, 20, 100]:
    # Calcular aproximaciones
    res_trapecio = metodo_trapecio(f, a, b, n)
    res_simpson = metodo_simpson(f, a, b, n)

    # Calcular errores absolutos: |Valor Exacto - Valor Aproximado|
    error_trapecio = abs(valor_exacto - res_trapecio)
    error_simpson = abs(valor_exacto - res_simpson)

    # Mostrar resultados formateados en columnas
    print(f"{n:<15}{error_trapecio:<20.10e}{error_simpson:<20.10e}")