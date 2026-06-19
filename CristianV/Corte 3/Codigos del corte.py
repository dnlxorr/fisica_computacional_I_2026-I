import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ================================================================
# 1. FUNCIONES DE PRUEBA (1D) Y SUS DERIVADAS EXACTAS
# ================================================================
def f2(x):
    return np.exp(-x) * np.sin(2*x)

def df2(x):
    return np.exp(-x) * (2*np.cos(2*x) - np.sin(2*x))

def d2f2(x):
    return np.exp(-x) * (-3*np.sin(2*x) - 4*np.cos(2*x))

# ================================================================
# 2. FUNCIÓN DE PRUEBA (2D) Y SUS DERIVADAS PARCIALES EXACTAS
# ================================================================
def g2(x, y):
    return x**2 + y**2 + x*y

def dg2_dx(x, y):
    return 2*x + y

def dg2_dy(x, y):
    return 2*y + x

# ================================================================
# 3. ESQUEMAS NUMÉRICOS
# ================================================================
def forward_diff(f, x, h):
    return (f(x + h) - f(x)) / h

def central_diff(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

def second_central_diff(f, x, h):
    return (f(x + h) - 2*f(x) + f(x - h)) / (h**2)

def partial_x_central(g, x, y, h):
    return (g(x + h, y) - g(x - h, y)) / (2 * h)

def partial_y_central(g, x, y, h):
    return (g(x, y + h) - g(x, y - h)) / (2 * h)

# ================================================================
# 4. APLICACIÓN: DERIVADAS, ERRORES Y ESTUDIO CON h VARIABLE
# ================================================================
print("===== CÓDIGO 2: TODOS LOS TEMAS =====")

x0 = 1.0
h_vals = np.logspace(-5, -1, 6)

print("\n--- 4a. Primera derivada (dif. finitas vs central) ---")
for h in h_vals:
    fd = forward_diff(f2, x0, h)
    cd = central_diff(f2, x0, h)
    exact = df2(x0)
    print(f"h={h:.1e}  |  Error FD={abs(fd-exact):.2e}  |  Error CD={abs(cd-exact):.2e}")

print("\n--- 4b. Segunda derivada con diferencias centrales ---")
h2 = 0.005
d2_num = second_central_diff(f2, x0, h2)
d2_ex = d2f2(x0)
print(f"x={x0}, h={h2}  →  Numérica={d2_num:.6f}, Exacta={d2_ex:.6f}, Error={abs(d2_num-d2_ex):.2e}")

print("\n--- 4c. Derivadas parciales (centrales) en 2D ---")
xp, yp = 2.0, 1.5
hp = 1e-5
px = partial_x_central(g2, xp, yp, hp)
py = partial_y_central(g2, xp, yp, hp)
ex_px = dg2_dx(xp, yp)
ex_py = dg2_dy(xp, yp)
print(f"En ({xp},{yp}), h={hp}:")
print(f"  ∂g/∂x → Num={px:.8f}, Exacta={ex_px:.8f}, Error={abs(px-ex_px):.2e}")
print(f"  ∂g/∂y → Num={py:.8f}, Exacta={ex_py:.8f}, Error={abs(py-ex_py):.2e}")

# ================================================================
# 5. INTERPOLACIÓN LINEAL Y SPLINE CÚBICO
# ================================================================
print("\n--- 5. Interpolación lineal y spline cúbico ---")
x_data = np.linspace(0, 4, 15)
y_data = f2(x_data)

x_fine = np.linspace(0, 4, 300)
y_exact = f2(x_fine)

# Lineal
y_lin = np.interp(x_fine, x_data, y_data)

# Spline cúbico natural
cs = CubicSpline(x_data, y_data, bc_type='natural')
y_spline = cs(x_fine)

err_lin_max = np.max(np.abs(y_lin - y_exact))
err_spline_max = np.max(np.abs(y_spline - y_exact))
print(f"Error máximo (lineal)  = {err_lin_max:.4f}")
print(f"Error máximo (spline)  = {err_spline_max:.4f}")

# Además, el spline nos permite evaluar derivadas numéricamente
cs_deriv1 = cs.derivative()
cs_deriv2 = cs.derivative(2)
d1_spline_en_nodos = cs_deriv1(x_data)
d2_spline_en_nodos = cs_deriv2(x_data)
print("\n--- Derivadas del spline evaluadas en los nodos (comparación) ---")
err_d1_spl = np.max(np.abs(d1_spline_en_nodos - df2(x_data)))
err_d2_spl = np.max(np.abs(d2_spline_en_nodos - d2f2(x_data)))
print(f"Error máximo en 1ª derivada (spline) = {err_d1_spl:.2e}")
print(f"Error máximo en 2ª derivada (spline) = {err_d2_spl:.2e}")

# ================================================================
# 6. GRÁFICA (opcional)
# ================================================================
plt.figure(figsize=(10, 6))
plt.plot(x_data, y_data, 'ok', label='Datos')
plt.plot(x_fine, y_exact, 'b-', label='Función exacta')
plt.plot(x_fine, y_lin, 'r--', label='Lineal')
plt.plot(x_fine, y_spline, 'g-', label='Spline cúbico')
plt.legend()
plt.title("Código 2 - Interpolación lineal y spline")
plt.grid(True)
plt.show()