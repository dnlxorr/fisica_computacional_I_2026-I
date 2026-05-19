import random


def integral_doble_montecarlo(f, ax, bx, ay, by, num_puntos):

    area_base = (bx - ax) * (by - ay)

    suma_alturas = 0.0


    for _ in range(num_puntos):

        x_aleatorio = random.uniform(ax, bx)


        y_aleatorio = random.uniform(ay, by)

        # Evaluamos la altura de la función en ese punto aleatorio
        suma_alturas += f(x_aleatorio, y_aleatorio)

    altura_promedio = suma_alturas / num_puntos
    integral = area_base * altura_promedio

    return integral

def mi_superficie(x, y):
    return x * y

lim_inf_x, lim_sup_x = 0, 2
lim_inf_y, lim_sup_y = 0, 3


puntos_azar = 100000


resultado = integral_doble_montecarlo(mi_superficie, lim_inf_x, lim_sup_x, lim_inf_y, lim_sup_y, puntos_azar)

print(f"Resultado aproximado con Montecarlo: {resultado:.6f}")
