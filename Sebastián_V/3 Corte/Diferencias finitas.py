import numpy as np

# Función de prueba
def f1(x):
    return x**3 - 2*x + 1

# Esquema numérico: diferencias finitas hacia adelante (orden 1)
def forward_diff(f, x, h):
    return (f(x + h) - f(x)) / h

# Demostración
x = 1.5
h = 0.01
derivada_num = forward_diff(f1, x, h)

print("===== DIFERENCIAS FINITAS (HACIA ADELANTE) =====")
print(f"f(x) = x^3 - 2x + 1")
print(f"x = {x}, h = {h}")
print(f"Derivada numérica (adelante) = {derivada_num:.6f}")