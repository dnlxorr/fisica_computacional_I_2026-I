import numpy as np
from scipy.interpolate import CubicSpline

# Función de prueba
def f1(x):
    return x**3 - 2*x + 1

# Datos discretos (pocos puntos)
x_data = np.linspace(0, 3, 10)
y_data = f1(x_data)

# Puntos finos para evaluar la interpolación
x_fine = np.linspace(0, 3, 200)
y_exact = f1(x_fine)

# Construcción del spline cúbico natural
cs = CubicSpline(x_data, y_data, bc_type='natural')
y_spline = cs(x_fine)

# Cálculo del error
error_max = np.max(np.abs(y_spline - y_exact))
error_rms = np.sqrt(np.mean((y_spline - y_exact)**2))

print("===== SPLINE CÚBICO =====")
print(f"Número de puntos discretos: {len(x_data)}")
print(f"Tipo de spline: natural (bc_type='natural')")
print(f"Error máximo  = {error_max:.4f}")
print(f"Error RMS     = {error_rms:.4f}")