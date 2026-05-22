# ----------------------------------------------------------
# REGLA DEL TRAPECIO
# ----------------------------------------------------------
# Este programa calcula una integral usando
# el método numérico de la Regla del Trapecio.
#
# La integral que vamos a resolver es:
#
# ∫ x² dx
#
# La función será:
# f(x) = x²
#
# Fórmula del trapecio:
#
# h = (b - a) / n
#
# Integral ≈ (h/2) * [f(a) + 2f(x1) + 2f(x2) + ... + f(b)]
# ----------------------------------------------------------

# Definimos la función
def f(x):

    # Retornamos x elevado al cuadrado
    return x**2


# Pedimos el límite inferior
a = float(input("Ingrese el límite inferior: "))

# Pedimos el límite superior
b = float(input("Ingrese el límite superior: "))

# Pedimos el número de intervalos
n = int(input("Ingrese el número de intervalos: "))

# Calculamos el tamaño de cada intervalo
# h significa "ancho" del trapecio
h = (b - a) / n

# Empezamos la suma con los extremos
suma = f(a) + f(b)

# Ciclo for
# Sirve para repetir varias veces
#
# range(1, n) significa:
# empezar en 1 y terminar en n-1
for i in range(1, n):

    # Calculamos el punto actual
    x = a + i * h

    # Sumamos 2*f(x)
    suma = suma + 2 * f(x)

# Aplicamos la fórmula final
integral = (h / 2) * suma

# Mostramos el resultado
print("La integral aproximada es:", integral)