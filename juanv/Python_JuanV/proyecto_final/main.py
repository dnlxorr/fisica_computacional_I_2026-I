import numpy as np
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

from physics_model import *
from numerical_methods import *
from wave_simulation import *

# =====================================================
# DATOS DE ENTRADA
# =====================================================

T = float(input("Temperatura atmosférica (°C): "))

f0 = 500

v0 = 100
a = 10

x0 = -2500

dt = 0.05
t_final = 40

t = np.arange(0, t_final, dt)

# =====================================================
# MODELO FÍSICO
# =====================================================

c = speed_of_sound(T)

v = aircraft_velocity(v0, a, t)

x_plane = aircraft_position(x0, v0, a, t)

mach = mach_number(v, c)

f_obs = []

for i in range(len(t)):

    if x_plane[i] < 0:
        f = doppler_frequency(
            f0, c, v[i], True
        )
    else:
        f = doppler_frequency(
            f0, c, v[i], False
        )

    f_obs.append(f)

f_obs = np.array(f_obs)

# =====================================================
# MÉTODOS NUMÉRICOS
# =====================================================

df = centered_difference(f_obs, dt)

t_spline, f_spline = spline_interpolation(
    t,
    f_obs
)

# =====================================================
# RESULTADOS
# =====================================================

print("\n===== RESULTADOS =====")

print(f"Velocidad del sonido: {c:.2f} m/s")
print(f"Mach máximo: {mach.max():.2f}")
print(f"Frecuencia máxima: {f_obs.max():.2f} Hz")

# =====================================================
# SIMULACIÓN 3D
# =====================================================

fig = plt.figure(figsize=(10, 8))

ax = fig.add_subplot(111, projection='3d')

surface = [None]

emitted_waves = []


def update(frame):

    ax.clear()

    # emitir nueva onda

    if frame % 5 == 0:

        emitted_waves.append(
            (
                x_plane[frame],
                0,
                t[frame]
            )
        )

    Z = generate_wave_field(
        X,
        Y,
        emitted_waves,
        c,
        t[frame]
    )

    ax.plot_surface(
        X,
        Y,
        Z,
        cmap='viridis',
        edgecolor='none'
    )

    # posición avión

    ax.scatter(
        x_plane[frame],
        0,
        2,
        color='red',
        s=80,
        label='Aeronave'
    )

    # observador

    ax.scatter(
        0,
        0,
        2,
        color='black',
        s=80,
        label='Observador'
    )

    ax.set_xlim(-3000, 3000)
    ax.set_ylim(-3000, 3000)
    ax.set_zlim(0, 4)

    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("Amplitud")

    ax.set_title(
        f"t={t[frame]:.1f} s\n"
        f"Mach={mach[frame]:.2f} | "
        f"Frecuencia={f_obs[frame]:.1f} Hz"
    )

    ax.view_init(elev=35, azim=-60)

    ax.legend()


ani = FuncAnimation(
    fig,
    update,
    frames=len(t),
    interval=50
)

plt.show()

# =====================================================
# GRÁFICAS CIENTÍFAS
# =====================================================

plt.figure(figsize=(8, 4))
plt.plot(t, v)
plt.axhline(c, linestyle="--")
plt.grid()
plt.xlabel("Tiempo (s)")
plt.ylabel("Velocidad (m/s)")
plt.title("Velocidad de la aeronave")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t, mach)
plt.axhline(1, linestyle="--")
plt.grid()
plt.xlabel("Tiempo (s)")
plt.ylabel("Número de Mach")
plt.title("Número de Mach")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t_spline, f_spline)
plt.grid()
plt.xlabel("Tiempo (s)")
plt.ylabel("Frecuencia (Hz)")
plt.title("Frecuencia percibida")
plt.show()

plt.figure(figsize=(8, 4))
plt.plot(t, df)
plt.grid()
plt.xlabel("Tiempo (s)")
plt.ylabel("df/dt")
plt.title("Derivada temporal de la frecuencia")
plt.show()