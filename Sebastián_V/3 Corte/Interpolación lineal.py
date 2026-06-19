import numpy as np

# Función de prueba
def f1(x):
    return x**3 - 2*x + 1

# Datos discretos (pocos puntos)
x_data = np.linspace(0, 3, 10)
y_data = f1(x_data)

# Puntos finos para evaluar la interpolación
x_fine = np.linspace(0, 3, 200)
y_exact = f1(x_fine)

# Interpolación lineal con NumPy
y_lin = np.interp(x_fine, x_data, y_data)

# Cálculo del error
error_max = np.max(np.abs(y_lin - y_exact))
error_rms = np.sqrt(np.mean((y_lin - y_exact)**2))

print("===== INTERPOLACIÓN LINEAL =====")
print(f"Número de puntos discretos: {len(x_data)}")
print(f"Puntos de evaluación finos: {len(x_fine)}")
print(f"Error máximo  = {error_max:.4f}")
print(f"Error RMS     = {error_rms:.4f}")