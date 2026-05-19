def metodo_simpson(f, a, b, n):

    if n % 2 != 0:
        raise ValueError("El número de subintervalos 'n' debe ser un número par.")

    # 1. Calcular el ancho de cada paso
    h = (b - a) / n

    # 2. Iniciar la suma con los extremos f(a) y f(b)
    suma = f(a) + f(b)

    # 3. Sumar los puntos intermedios con sus respectivos pesos (4 o 2)
    for i in range(1, n):
        x = a + i * h

        if i % 2 != 0:
            # Posición impar: se multiplica por 4
            suma += 4 * f(x)
        else:
            # Posición par: se multiplica por 2
            suma += 2 * f(x)

    # 4. Multiplicar por el ancho h y dividir entre 3
    integral = (h / 3) * suma

    return integral





def mi_funcion(x):
    return x ** 2



limite_inferior = 0  # Punto 'a'
limite_superior = 3  # Punto 'b'
num_intervalos = 10  # Usamos solo 10 para ver su enorme precisión


resultado = metodo_simpson(mi_funcion, limite_inferior, limite_superior, num_intervalos)

print(f"Resultado aproximado con Simpson: {resultado}")
