# ----------------------------------------------------------
# REGLA DE SIMPSON
# ----------------------------------------------------------
# Este método usa parábolas para aproximar
# el área bajo la curva.
#
# Fórmula:
#
# Integral ≈ (h/3) * [f(a) + 4f(x1) + 2f(x2) + ... + f(b)]
#
# IMPORTANTE:
# n debe ser PAR
# ----------------------------------------------------------

def f(x):

    # Función x²
    return x**2


a = float(input("Ingrese el límite inferior: "))
b = float(input("Ingrese el límite superior: "))
n = int(input("Ingrese el número de intervalos PAR: "))

# Verificamos si n es impar
#
# El operador % obtiene el residuo
# Si el residuo es diferente de 0,
# entonces el número es impar
if n % 2 != 0:

    print("El número de intervalos debe ser PAR")

else:

    h = (b - a) / n

    suma = f(a) + f(b)

    for i in range(1, n):

        x = a + i * h

        # Si i es impar
        if i % 2 != 0:

            suma = suma + 4 * f(x)

        # Si i es par
        else:

            suma = suma + 2 * f(x)

    integral = (h / 3) * suma

    print("La integral aproximada es:", integral)