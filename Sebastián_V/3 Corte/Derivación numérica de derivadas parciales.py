import numpy as np

# Función de prueba 2D y sus derivadas parciales exactas
def g1(x, y):
    return np.sin(x) * np.cos(y)

def dg1_dx(x, y):
    return np.cos(x) * np.cos(y)

def dg1_dy(x, y):
    return -np.sin(x) * np.sin(y)

# Esquemas numéricos para derivadas parciales (diferencias centrales)
def partial_x_central(g, x, y, h):
    return (g(x + h, y) - g(x - h, y)) / (2 * h)

def partial_y_central(g, x, y, h):
    return (g(x, y + h) - g(x, y - h)) / (2 * h)

# Demostración
x, y = 0.8, 1.2
h = 1e-4

px_num = partial_x_central(g1, x, y, h)
py_num = partial_y_central(g1, x, y, h)
px_ex = dg1_dx(x, y)
py_ex = dg1_dy(x, y)

print("===== DERIVADAS PARCIALES NUMÉRICAS =====")
print(f"g(x,y) = sin(x)*cos(y)")
print(f"Punto (x, y) = ({x}, {y}),  h = {h}\n")
print(f"∂g/∂x → Numérica = {px_num:.8f}, Exacta = {px_ex:.8f}, Error = {abs(px_num - px_ex):.2e}")
print(f"∂g/∂y → Numérica = {py_num:.8f}, Exacta = {py_ex:.8f}, Error = {abs(py_num - py_ex):.2e}")