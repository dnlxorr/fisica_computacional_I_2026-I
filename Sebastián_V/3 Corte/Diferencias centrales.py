import numpy as np

# Función de prueba
def f1(x):
    return x**3 - 2*x + 1

# Esquema numérico: diferencias centrales (orden 2)
def central_diff(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

# Demostración
x = 1.5
h = 0.01
derivada_num = central_diff(f1, x, h)

print("===== DIFERENCIAS CENTRALES =====")
print(f"f(x) = x^3 - 2x + 1")
print(f"x = {x}, h = {h}")
print(f"Derivada numérica (central) = {derivada_num:.6f}")