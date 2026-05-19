def metodo_trapecio(f, a, b, n):


    h = (b - a) / n


    suma = f(a) + f(b)

   
    for i in range(1, n):
        x = a + i * h
        suma += 2 * f(x)


    integral = (h / 2) * suma

    return integral





def mi_funcion(x):
    return x ** 2



limite_inferior = 0
limite_superior = 3
num_trapecios = 100


resultado = metodo_trapecio(mi_funcion, limite_inferior, limite_superior, num_trapecios)

print(f"El resultado aproximado de la integral es: {resultado}")
