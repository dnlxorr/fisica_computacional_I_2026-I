def trapecio_adaptativo(f, a, b, tol):


    h = b - a
    area_un_paso = (h / 2) * (f(a) + f(b))


    c = (a + b) / 2
    area_dos_pasos = (h / 4) * (f(a) + 2 * f(c) + f(b))


    error_estimado = abs(area_dos_pasos - area_un_paso) / 3


    if error_estimado <= tol:

        return area_dos_pasos
    else:

        mitad_izquierda = trapecio_adaptativo(f, a, c, tol / 2)
        mitad_right = trapecio_adaptativo(f, c, b, tol / 2)

        # Sumamos los resultados de ambas mitades
        return mitad_izquierda + mitad_right




def mi_funcion(x):
    return 1 / (x ** 2)


limite_inferior = 0.5
limite_superior = 4.0
tolerancia_maxima = 1e-6  # Queremos una precisión de 6 decimales

# Llamada a la función
resultado = trapecio_adaptativo(mi_funcion, limite_inferior, limite_superior, tolerancia_maxima)

print(f"Resultado de la integración adaptativa: {resultado:.6f}")
# El valor analítico exacto de esta integral es 1.75