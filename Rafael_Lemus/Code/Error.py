import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline

# =====================================================
# Cargar dataset
# =====================================================

df = pd.read_csv("dataset_orbita_marte_spline.csv")

t = df["dia"].values
x = df["x_AU"].values
y = df["y_AU"].values

# =====================================================
# Splines
# =====================================================

sx = CubicSpline(t, x)
sy = CubicSpline(t, y)

t_dense = np.linspace(t.min(), t.max(), 5000)

# reconstrucción
x_num = sx(t_dense)
y_num = sy(t_dense)

vx_num = sx(t_dense, 1)
vy_num = sy(t_dense, 1)

ax_num = sx(t_dense, 2)
ay_num = sy(t_dense, 2)

# =====================================================
# Órbita de referencia
# =====================================================

a = 1.524
e = 0.0934
T = 687.0

M = 2*np.pi*t_dense/T

E = M.copy()

for _ in range(15):
    E = E - (E - e*np.sin(E) - M)/(1 - e*np.cos(E))

# posición exacta

x_ref = a*(np.cos(E) - e)
y_ref = a*np.sqrt(1-e**2)*np.sin(E)

# derivadas exactas

dEdt = (2*np.pi/T)/(1 - e*np.cos(E))

vx_ref = -a*np.sin(E)*dEdt

vy_ref = (
    a*np.sqrt(1-e**2)
    *np.cos(E)
    *dEdt
)

# aceleraciones exactas

ddEdt = (
    -(2*np.pi/T)**2
    *e*np.sin(E)
    /(1-e*np.cos(E))**3
)

ax_ref = (
    -a*np.cos(E)*dEdt**2
    -a*np.sin(E)*ddEdt
)

ay_ref = (
    -a*np.sqrt(1-e**2)
    *np.sin(E)
    *dEdt**2
    +
    a*np.sqrt(1-e**2)
    *np.cos(E)
    *ddEdt
)

# =====================================================
# Magnitudes
# =====================================================

r_num = np.sqrt(x_num**2 + y_num**2)
r_ref = np.sqrt(x_ref**2 + y_ref**2)

v_num = np.sqrt(vx_num**2 + vy_num**2)
v_ref = np.sqrt(vx_ref**2 + vy_ref**2)

a_num = np.sqrt(ax_num**2 + ay_num**2)
a_ref = np.sqrt(ax_ref**2 + ay_ref**2)

# =====================================================
# Error relativo medio (%)
# =====================================================

err_r = np.mean(
    np.abs((r_num-r_ref)/r_ref)
)*100

err_v = np.mean(
    np.abs((v_num-v_ref)/v_ref)
)*100

err_a = np.mean(
    np.abs((a_num-a_ref)/a_ref)
)*100

# =====================================================
# Salida para tabla REVTeX
# =====================================================

print("\nTABLA LATEX\n")

print(
f"Posición & {err_r:.4f} \\\\"
)

print(
f"Velocidad & {err_v:.4f} \\\\"
)

print(
f"Aceleración & {err_a:.4f} \\\\"
)