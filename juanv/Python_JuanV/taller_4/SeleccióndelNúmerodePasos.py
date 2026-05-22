# ----------------------------------------------------------
# SELECCIÓN DEL NÚMERO DE PASOS
# ----------------------------------------------------------
# Este programa muestra cómo cambia
# la precisión usando diferentes valores de n.
# ----------------------------------------------------------

def f(x):

    return x**2


a = 0
b = 2

# Lista de pasos
# Probamos varios valores de n
pasos = [2, 4, 8, 16]

for n in pasos:

    h = (b - a) / n

    suma = f(a) + f(b)

    for i in range(1, n):

        x = a + i * h

        suma = suma + 2 * f(x)

    integral = (h / 2) * suma

    print("Con n =", n)
    print("Integral =", integral)
    print("----------------")