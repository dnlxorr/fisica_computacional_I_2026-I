def integracion_infina_simple(n):


    # 1. Definimos la función matemática original: f(x) = 1 / x^2
    def f(x):
        return 1 / (x ** 2)


    def f_transformada(t):
        if t == 0:
            return 0  # Evitamos la división por cero en el extremo exacto
        return f(1 / t) * (1 / (t ** 2))

    a = 0
    b = 1
    h = (b - a) / n

    suma = f_transformada(a) + f_transformada(b)

    for i in range(1, n):
        t = a + i * h
        suma += 2 * f_transformada(t)

    integral = (h / 2) * suma
    return integral




num_pasos = 1000
resultado = integracion_infina_simple(num_pasos)

print(f"Resultado de la integral al infinito: {resultado:.6f}")
# El valor teórico exacto es 1.0