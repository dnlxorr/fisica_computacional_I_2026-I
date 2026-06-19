# =========================
# Simulación Caso1
# =========================
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

# =========================
# PARÁMETROS FÍSICOS
# =========================
c = 1.0
gamma = 0.02

# =========================
# DOMINIO
# =========================
L = 10

Nx = Ny = 200
dx = L / Nx

x = np.linspace(-L/2, L/2, Nx)
y = np.linspace(-L/2, L/2, Ny)

X, Y = np.meshgrid(x, y)

# =========================
# TIEMPO
# =========================
dt = 0.005
T = 25
Nt = int(T / dt)

# Momento en que ocurre el impacto
impact_step = 200

# =========================
# LAPLACIANO
# =========================
def laplacian(u):
    return (
        np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
        - 4*u
    ) / dx**2


# =========================
# FRONTERAS REFLECTIVAS
# =========================
def boundaries(u):

    u[0, :] = u[1, :]
    u[-1, :] = u[-2, :]

    u[:, 0] = u[:, 1]
    u[:, -1] = u[:, -2]

    return u


# =========================
# ENERGÍA
# =========================
def energy(u, u_prev):

    du_dt = (u - u_prev) / dt

    grad = (
        np.gradient(u, dx, axis=0)**2
        + np.gradient(u, dx, axis=1)**2
    )

    Ek = 0.5 * du_dt**2
    Ep = 0.5 * c**2 * grad

    return np.sum(Ek + Ep) * dx * dx


# =========================
# AGUA QUIETA
# =========================
u_old = np.zeros((Ny, Nx))
u_current = np.zeros((Ny, Nx))
u_new = np.zeros((Ny, Nx))

# =========================
# FIGURA
# =========================
fig = plt.figure(figsize=(12,5))

ax1 = fig.add_subplot(1,2,1, projection='3d')
ax2 = fig.add_subplot(1,2,2)

energy_list = []
time_list = []

# =========================
# LOOP PRINCIPAL
# =========================
for n in range(Nt):

    # =====================
    # IMPACTO DE LA PIEDRA
    # =====================
    if n == impact_step:

        sigma = 0.8

        impacto = np.exp(
            -(X**2 + Y**2)/(2*sigma**2)
        )

        u_current += impacto
        u_old += impacto

    lap = laplacian(u_current)

    u_new = (
        2*u_current
        - u_old
        + (c**2 * dt**2)*lap
        - gamma*dt*(u_current-u_old)
    )

    u_new = boundaries(u_new)

    # =====================
    # ENERGÍA
    # =====================
    E = energy(u_new, u_current)

    energy_list.append(E)
    time_list.append(n*dt)

    # =====================
    # VISUALIZACIÓN
    # =====================
    if n % 25 == 0:

        ax1.clear()

        ax1.plot_surface(
            X,
            Y,
            u_new,
            cmap=cm.viridis
        )

        tiempo = n * dt

        ax1.set_title(
            f"Caso 1 - Impacto Central | t = {tiempo:.2f}"
        )

        ax1.set_xlabel("x")
        ax1.set_ylabel("y")
        ax1.set_zlabel("u")

        ax1.set_zlim(-1, 1)

        ax2.clear()

        ax2.plot(
            time_list,
            energy_list,
            'b'
        )

        ax2.set_title(
            "Energía total del sistema"
        )

        ax2.set_xlabel("t")
        ax2.set_ylabel("E(t)")

        ax2.grid(True)

        plt.pause(0.001)

    u_old = u_current.copy()
    u_current = u_new.copy()

plt.show()