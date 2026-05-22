import numpy as np

# -----------------------------
# función de dos variables
# -----------------------------
def f(x, y):
    return x + y

# -----------------------------
# integración doble tipo Riemann
# -----------------------------
def integral_doble(f, ax, bx, ay, by, nx=200, ny=200):
    """
    Aproxima la integral doble:
    ∬ f(x,y) dy dx
    usando suma de Riemann en malla 2D
    """

    # discretización en x y y
    x = np.linspace(ax, bx, nx)
    y = np.linspace(ay, by, ny)

    dx = (bx - ax) / (nx - 1)
    dy = (by - ay) / (ny - 1)

    suma = 0.0

    # doble suma
    for xi in x:
        for yj in y:
            suma += f(xi, yj)

    # multiplicamos por el área del rectángulo elemental
    return suma * dx * dy


# -----------------------------
# límites de integración
# -----------------------------
resultado = integral_doble(f, 0, 1, 0, 2)

print("Resultado integral doble:", resultado)