import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ==========================
# Cargar datos
# ==========================
df = pd.read_csv("dataset_orbita_marte_spline.csv")

t = df["dia"].values
x = df["x_AU"].values
y = df["y_AU"].values

# ==========================
# Splines cúbicos
# ==========================
sx = CubicSpline(t, x)
sy = CubicSpline(t, y)

t_dense = np.linspace(t.min(), t.max(), 5000)

x_dense = sx(t_dense)
y_dense = sy(t_dense)

vx = sx(t_dense, 1)
vy = sy(t_dense, 1)

ax = sx(t_dense, 2)
ay = sy(t_dense, 2)

v = np.sqrt(vx**2 + vy**2)
a = np.sqrt(ax**2 + ay**2)


plt.figure(figsize=(8,5))

plt.plot(
    t_dense,
    ax,
    label=r"$a_x$"
)

plt.plot(
    t_dense,
    ay,
    label=r"$a_y$"
)

plt.xlabel("Tiempo (días)")
plt.ylabel("Aceleración (UA/día$^2$)")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig(
    "aceleracion_componentes.png",
    dpi=300
)
plt.show()