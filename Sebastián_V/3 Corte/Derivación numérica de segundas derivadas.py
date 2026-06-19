import numpy as np

# Función de prueba y su segunda derivada exacta
def f1(x):
    return x**3 - 2*x + 1

def d2f1(x):
    return 6*x

# Esquema numérico: segunda derivada con diferencias centrales
def second_central_diff(f, x, h):
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

# Demostración
x = 1.5
h = 0.01
num = second_central_diff(f1, x, h)
exacta = d2f1(x)

print("===== SEGUNDA DERIVADA NUMÉRICA =====")
print(f"f(x) = x^3 - 2x + 1")
print(f"x = {x}, h = {h}")
print(f"Segunda derivada numérica = {num:.6f}")
print(f"Segunda derivada exacta   = {exacta:.6f}")
print(f"Error absoluto            = {abs(num - exacta):.2e}")