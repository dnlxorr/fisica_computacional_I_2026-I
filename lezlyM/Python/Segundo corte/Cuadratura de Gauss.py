def cuadratura_gauss(f, a, b, puntos=3):

    if puntos == 2:
        # Raíces de un polinomio de Legendre de grado 2
        nodos = [-0.5773502691896257, 0.5773502691896257]  # -1/sqrt(3) y 1/sqrt(3)
        pesos = [1.0, 1.0]
    elif puntos == 3:
        # Raíces de un polinomio de Legendre de grado 3
        nodos = [-0.7745966692414834, 0.0, 0.7745966692414834]
        pesos = [0.5555555555555556, 0.8888888888888888, 0.5555555555555556]  # 5/9, 8/9, 5/9
    else:
        raise ValueError("Este código simple solo soporta 2 o 3 puntos.")

    suma = 0.0

    for t, w in zip(nodos, pesos):
        # Transformar el punto 't' (de -1 a 1) en un punto 'x' (de a a b)
        x = ((b - a) * t + (a + b)) / 2

        # Sumar el peso multiplicado por el valor de la función en ese 'x'
        suma += w * f(x)


    integral = ((b - a) / 2) * suma

    return integral



import math


def mi_funcion(x):
    return math.exp(x)


limite_inferior = 0  # Punto 'a'
limite_superior = 2  # Punto 'b'



resultado = cuadratura_gauss(mi_funcion, limite_inferior, limite_superior, puntos=3)

print(f"Resultado con 3 puntos de Gauss: {resultado:.10f}")
print(f"Valor exacto real de la integral: {6.3890560989:.10f}")
