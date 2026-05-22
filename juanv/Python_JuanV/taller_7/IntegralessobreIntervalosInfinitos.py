# ----------------------------------------------------------
# INTEGRALES EN INTERVALOS INFINITOS
# ----------------------------------------------------------
# Vamos a aproximar:
#
# ∫ 1/x² dx
#
# desde 1 hasta infinito.
#
# En programación usamos un número grande
# para representar infinito.
# ----------------------------------------------------------

def f(x):

    return 1 / (x**2)


a = 1

# Usamos 1000 como aproximación de infinito
b = 1000

n = 100

h = (b - a) / n

suma = f(a) + f(b)

for i in range(1, n):

    x = a + i * h

    suma = suma + 2 * f(x)

integral = (h / 2) * suma

print("Integral aproximada:", integral)