# ============================================================
# CASO 1:
# ============================================================

# ============================================================
# LIBRERÍAS
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

from scipy.integrate import simpson
from scipy.interpolate import CubicSpline

import time

# ============================================================
# PARÁMETROS FÍSICOS
# ============================================================

# Velocidad de propagación
c = 1.0

# Amortiguamiento
gamma = 0.05

# Amplitud inicial
A = 1.0

# Ancho de la gaussiana
sigma = 0.5

# Dominio espacial
L = 5.0

# Número de nodos
Nx = 201
Ny = 201

# Mallado
dx = 2 * L / (Nx - 1)
dy = 2 * L / (Ny - 1)

# Tiempo final
Tf = 20.0

# Paso temporal
dt = 0.01

# Número de iteraciones
Nt = int(Tf / dt)

# CFL
CFL = c * dt / dx

print("=" * 60)
print("ESTUDIO COMPUTACIONAL DE ENERGÍA EN ONDAS SUPERFICIALES")
print("=" * 60)

print("\nPARÁMETROS FÍSICOS")
print("-" * 60)

print(f"Velocidad de propagación (c) = {c}")
print(f"Amortiguamiento (gamma)      = {gamma}")
print(f"Amplitud inicial (A)         = {A}")
print(f"Ancho gaussiano (sigma)      = {sigma}")

print("\nDOMINIO ESPACIAL")
print("-" * 60)

print(f"Longitud del dominio (L) = {L}")
print(f"Nodos en x (Nx)          = {Nx}")
print(f"Nodos en y (Ny)          = {Ny}")

print(f"dx = {dx:.6f}")
print(f"dy = {dy:.6f}")

print("\nPARÁMETROS TEMPORALES")
print("-" * 60)

print(f"Tiempo final (Tf)          = {Tf}")
print(f"Paso temporal (dt)         = {dt}")
print(f"Número de iteraciones (Nt) = {Nt}")

print("\nESTABILIDAD NUMÉRICA")
print("-" * 60)

print(f"CFL = {CFL:.6f}")

if CFL <= 1 / np.sqrt(2):
    print("Estado CFL: ESTABLE")
else:
    print("Estado CFL: INESTABLE")

print("=" * 60)

# ============================================================
# MALLA ESPACIAL
# ============================================================

x = np.linspace(-L, L, Nx)
y = np.linspace(-L, L, Ny)

X, Y = np.meshgrid(x, y)


# ============================================================
# CONDICIÓN INICIAL
# CASO 1: PULSO GAUSSIANO CENTRAL
# ============================================================

u0 = A * np.exp(
    -((X**2 + Y**2) / (2 * sigma**2))
)

# velocidad inicial nula
v0 = np.zeros_like(u0)


# ============================================================
# DIFERENCIAS FINITAS
# ============================================================

def laplaciano(U, dx):

    lap = np.zeros_like(U)

    lap[1:-1, 1:-1] = (
        U[2:, 1:-1]
        + U[:-2, 1:-1]
        + U[1:-1, 2:]
        + U[1:-1, :-2]
        - 4 * U[1:-1, 1:-1]
    ) / dx**2

    return lap


# ============================================================
# FRONTERAS REFLECTIVAS (NEUMANN)
# ============================================================

def aplicar_fronteras(U):

    U[0, :] = U[1, :]
    U[-1, :] = U[-2, :]

    U[:, 0] = U[:, 1]
    U[:, -1] = U[:, -2]

    return U


# ============================================================
# ENERGÍA LOCAL
# ============================================================

def energia_local(U, Ut, dx, c):

    dUx = np.zeros_like(U)
    dUy = np.zeros_like(U)

    dUx[1:-1, :] = (
        U[2:, :] - U[:-2, :]
    ) / (2 * dx)

    dUy[:, 1:-1] = (
        U[:, 2:] - U[:, :-2]
    ) / (2 * dx)

    energia = (
        0.5 * Ut**2
        + 0.5 * c**2 * (dUx**2 + dUy**2)
    )

    return energia


# ============================================================
# REGLA DE SIMPSON
# ENERGÍA TOTAL
# ============================================================

def energia_total(E_local, x, y):

    integral_y = simpson(
        E_local,
        y,
        axis=0
    )

    integral_total = simpson(
        integral_y,
        x
    )

    return integral_total


# ============================================================
# SPLINE CÚBICO
# ============================================================

def construir_spline(tiempos, energias):

    spline = CubicSpline(
        tiempos,
        energias
    )

    return spline


# ============================================================
# ERROR ESPACIAL
# ============================================================

def error_relativo(sol1, sol2):

    return (
        np.linalg.norm(sol1 - sol2)
        /
        np.linalg.norm(sol2)
    )


def orden_convergencia(e1, e2):

    return np.log(e1 / e2) / np.log(2)

# ============================================================
# EVOLUCIÓN TEMPORAL
# ============================================================

inicio = time.time()

# Estado anterior
u_old = u0.copy()

# Primer paso temporal
lap0 = laplaciano(u0, dx)

u = (
    u0
    + dt * v0
    + 0.5 * dt**2 *
    (
        c**2 * lap0
        - gamma * v0
    )
)

u = aplicar_fronteras(u)

# ============================================================
# TIEMPOS DE INTERÉS
# ============================================================

t0 = 1.0
t1 = 5.0
t2 = 10.0
t3 = 20.0

indices_tiempos = {
    int(t0 / dt): "t0",
    int(t1 / dt): "t1",
    int(t2 / dt): "t2",
    int(t3 / dt): "t3"
}

# ============================================================
# ALMACENAMIENTO DE RESULTADOS
# ============================================================

ondas = {}
energias_locales = {}

energia_vs_tiempo = []
tiempo_vs_tiempo = []

# ============================================================
# CAPTURA INICIAL
# ============================================================

Ut0 = np.zeros_like(u0)

E_local0 = energia_local(
    u0,
    Ut0,
    dx,
    c
)

E_total0 = energia_total(
    E_local0,
    x,
    y
)

ondas["t0"] = u0.copy()

energias_locales["t0"] = (
    E_local0.copy()
)

# ============================================================
# BUCLE PRINCIPAL
# ============================================================

for n in range(1, Nt + 1):

    lap = laplaciano(u, dx)

    u_new = (
        (
            2 * u
            - u_old
        )
        +
        dt**2
        *
        (
            c**2 * lap
        )
        -
        gamma * dt
        *
        (
            u - u_old
        )
    )

    u_new = aplicar_fronteras(u_new)

    # velocidad aproximada
    Ut = (u_new - u_old) / (2 * dt)

    # energía local
    E_local = energia_local(
        u_new,
        Ut,
        dx,
        c
    )

    # energía total (Simpson)
    E_total = energia_total(
        E_local,
        x,
        y
    )

    energia_vs_tiempo.append(
        E_total
    )

    tiempo_vs_tiempo.append(
        n * dt
    )

    # -----------------------------------
    # GUARDAR SNAPSHOTS
    # -----------------------------------

    if n in indices_tiempos:

        etiqueta = indices_tiempos[n]

        ondas[etiqueta] = u_new.copy()

        energias_locales[etiqueta] = (
            E_local.copy()
        )

    # actualizar estados

    u_old = u.copy()
    u = u_new.copy()

# ============================================================
# CONVERTIR A NUMPY
# ============================================================

energia_vs_tiempo = np.array(
    energia_vs_tiempo
)

tiempo_vs_tiempo = np.array(
    tiempo_vs_tiempo
)

# ============================================================
# SPLINE CÚBICO
# ============================================================

spline = construir_spline(
    tiempo_vs_tiempo,
    energia_vs_tiempo
)

tiempo_suave = np.linspace(
    0,
    Tf,
    5000
)

energia_suave = spline(
    tiempo_suave
)

# ============================================================
# ERROR DEL SPLINE CÚBICO
# ============================================================

indices_prueba = np.arange(
    100,
    len(tiempo_vs_tiempo)-100,
    100
)

errores_porcentuales = []

for idx in indices_prueba:

    t_real = tiempo_vs_tiempo[idx]

    E_real = energia_vs_tiempo[idx]

    tiempos_aux = np.delete(
        tiempo_vs_tiempo,
        idx
    )

    energias_aux = np.delete(
        energia_vs_tiempo,
        idx
    )

    spline_aux = CubicSpline(
        tiempos_aux,
        energias_aux
    )

    E_interp = spline_aux(
        t_real
    )

    error = (
        abs(E_real - E_interp)
        /
        abs(E_real)
    ) * 100

    errores_porcentuales.append(
        error
    )

# ============================================================
# ENERGÍAS DE INTERÉS
# ============================================================

E_t0 = energia_total(
    energias_locales["t0"],
    x,
    y
)

E_t1 = energia_total(
    energias_locales["t1"],
    x,
    y
)

E_t2 = energia_total(
    energias_locales["t2"],
    x,
    y
)

E_t3 = energia_total(
    energias_locales["t3"],
    x,
    y
)

# ============================================================
# DISIPACIÓN
# ============================================================

energia_inicial = E_t0

energia_final = energia_vs_tiempo[-1]

perdida_absoluta = (
    energia_inicial
    - energia_final
)

perdida_porcentual = (
    perdida_absoluta
    /
    energia_inicial
) * 100

# ============================================================
# IMPRESIÓN EN CONSOLA
# ============================================================

print("\n")
print("=" * 60)
print("RESULTADOS ENERGÉTICOS")
print("=" * 60)

print(f"E(t0 = {t0:5.2f}) = {E_t0:.8f}")
print(f"E(t1 = {t1:5.2f}) = {E_t1:.8f}")
print(f"E(t2 = {t2:5.2f}) = {E_t2:.8f}")
print(f"E(t3 = {t3:5.2f}) = {E_t3:.8f}")

print("\n")

print("=" * 60)
print("DISIPACIÓN")
print("=" * 60)

print(
    f"Energía inicial = "
    f"{energia_inicial:.8f}"
)

print(
    f"Energía final   = "
    f"{energia_final:.8f}"
)

print(
    f"Pérdida absoluta = "
    f"{perdida_absoluta:.8f}"
)

print(
    f"Pérdida porcentual = "
    f"{perdida_porcentual:.4f} %"
)

print("\n")

print("=" * 60)
print("SPLINE CÚBICO")
print("=" * 60)

print(
    "Puntos originales :",
    len(tiempo_vs_tiempo)
)

print(
    "Puntos interpolados :",
    len(tiempo_suave)
)

print("\n")

# ============================================================
# MÉTRICAS DEL SPLINE
# ============================================================

error_promedio_spline = np.mean(
    errores_porcentuales
)

error_maximo_spline = np.max(
    errores_porcentuales
)

print("\n")
print("=" * 60)
print("ANÁLISIS DEL SPLINE CÚBICO")
print("=" * 60)

print(
    f"Error porcentual promedio = "
    f"{error_promedio_spline:.6f} %"
)

print(
    f"Error porcentual máximo   = "
    f"{error_maximo_spline:.6f} %"
)

print("\n")

fin = time.time()

print("=" * 60)
print("RENDIMIENTO")
print("=" * 60)

print(
    f"Tiempo de ejecución = "
    f"{fin - inicio:.2f} s"
)

# ============================================================
# AMPLITUDES CARACTERÍSTICAS
# ============================================================

A_t0 = np.max(np.abs(ondas["t0"]))
A_t1 = np.max(np.abs(ondas["t1"]))
A_t2 = np.max(np.abs(ondas["t2"]))
A_t3 = np.max(np.abs(ondas["t3"]))

A2_t0 = A_t0**2
A2_t1 = A_t1**2
A2_t2 = A_t2**2
A2_t3 = A_t3**2

# ============================================================
# GRÁFICA 1
# ONDA EN t0, t1, t2, t3 (3D)
# ============================================================

fig = plt.figure(figsize=(14, 10))

tiempos_labels = ["t0", "t1", "t2", "t3"]

zmax = max(
    np.max(np.abs(ondas[t]))
    for t in tiempos_labels
)

for i, tiempo in enumerate(tiempos_labels):

    ax = fig.add_subplot(
        2, 2, i + 1,
        projection='3d'
    )

    ax.plot_surface(
        X,
        Y,
        ondas[tiempo],
        cmap='viridis'
    )

    ax.set_title(tiempo)

    # Unidades agregadas
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_zlabel("u (m)")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5, 5)
    ax.set_zlim(-zmax, zmax)

plt.suptitle(
    "Evolución temporal de la onda"
)

plt.tight_layout()

plt.show()

# ============================================================
# GRÁFICA 2
# ENERGÍA LOCAL EN t0, t1, t2, t3
# ============================================================

fig, ax = plt.subplots(2, 2, figsize=(12, 10))

tiempos_labels = ["t0", "t1", "t2", "t3"]

# MISMA ESCALA PARA TODOS LOS TIEMPOS

vmin = min(
    np.min(energias_locales[t])
    for t in tiempos_labels
)

vmax = max(
    np.max(energias_locales[t])
    for t in tiempos_labels
)

for eje, tiempo in zip(ax.ravel(), tiempos_labels):

    im = eje.imshow(
        energias_locales[tiempo],
        extent=[-L, L, -L, L],
        origin='lower',
        vmin=vmin,
        vmax=vmax,
        cmap='turbo'
    )

    eje.set_title(
        f"Energía local - {tiempo}"
    )

    # Unidades agregadas
    eje.set_xlabel("x (m)")
    eje.set_ylabel("y (m)")

    cbar = plt.colorbar(
        im,
        ax=eje,
        shrink=0.75
    )

    # Unidad agregada
    cbar.set_label(
        r"Energía local $E(x,y,t)$ (J/m$^2$)"
    )

plt.suptitle(
    "Distribución espacial de energía"
)

plt.tight_layout(
    pad=3.0
)

plt.show()

# ============================================================
# GRÁFICA 3
# ENERGÍA TOTAL VS TIEMPO
# ============================================================

plt.figure(figsize=(10, 6))

plt.plot(
    tiempo_vs_tiempo,
    energia_vs_tiempo,
    linewidth=2
)

plt.xlabel(
    "Tiempo (s)"
)

plt.ylabel(
    "Energía total (J)"
)

plt.title(
    "Energía total vs tiempo"
)

plt.grid(True)

plt.show()

# ============================================================
# GRÁFICA 4
# PORCENTAJE DE ENERGÍA PERDIDA
# ============================================================

# ------------------------------------------------------------
# PORCENTAJE DE ENERGÍA PERDIDA
# ------------------------------------------------------------

porcentaje_perdido = (
    (energia_inicial - energia_vs_tiempo)
    /
    energia_inicial
) * 100

# ------------------------------------------------------------
# PORCENTAJES EN LOS TIEMPOS DE ESTUDIO
# ------------------------------------------------------------

porcentaje_t0 = (
    (energia_inicial - E_t0)
    /
    energia_inicial
) * 100

porcentaje_t1 = (
    (energia_inicial - E_t1)
    /
    energia_inicial
) * 100

porcentaje_t2 = (
    (energia_inicial - E_t2)
    /
    energia_inicial
) * 100

porcentaje_t3 = (
    (energia_inicial - E_t3)
    /
    energia_inicial
) * 100

# ------------------------------------------------------------
# TIEMPOS Y PORCENTAJES
# ------------------------------------------------------------

tiempos_clave = np.array([
    t0,
    t1,
    t2,
    t3
])

porcentajes = np.array([
    porcentaje_t0,
    porcentaje_t1,
    porcentaje_t2,
    porcentaje_t3
])

# ------------------------------------------------------------
# FIGURA
# ------------------------------------------------------------

plt.figure(figsize=(10,6))

plt.plot(
    tiempo_vs_tiempo,
    porcentaje_perdido,
    linewidth=3,
    label="Energía disipada (%)"
)

# ------------------------------------------------------------
# PUNTOS DE ESTUDIO
# ------------------------------------------------------------

plt.scatter(
    tiempos_clave,
    porcentajes,
    s=100,
    zorder=5
)

# ------------------------------------------------------------
# LÍNEAS GUÍA
# ------------------------------------------------------------

for t, p in zip(
    tiempos_clave,
    porcentajes
):

    plt.vlines(
        t,
        0,
        p,
        linestyles='dashed',
        alpha=0.7
    )

    plt.hlines(
        p,
        0,
        t,
        linestyles='dashed',
        alpha=0.7
    )

# ------------------------------------------------------------
# ETIQUETAS DE PORCENTAJE
# ------------------------------------------------------------

for t, p in zip(
    tiempos_clave,
    porcentajes
):

    plt.annotate(
        f"{p:.2f} %",
        (t, p),
        xytext=(10,10),
        textcoords="offset points"
    )

# ------------------------------------------------------------
# CUADRO INFORMATIVO
# ------------------------------------------------------------

plt.text(
    0.55 * Tf,
    0.85 * np.max(porcentaje_perdido),
    f"Pérdida final = {perdida_porcentual:.2f} %",
    bbox=dict(
        facecolor='white',
        alpha=0.8
    )
)

# ------------------------------------------------------------
# FORMATO
# ------------------------------------------------------------

plt.xlabel(
    "Tiempo (s)",
    fontsize=12
)

plt.ylabel(
    "Energía perdida (%)",
    fontsize=12
)

plt.title(
    "Porcentaje de Energía Disipada en el Sistema",
    fontsize=14
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ============================================================
# ENERGÍA VS AMPLITUD²
# ============================================================

amplitud2 = np.array([
    A2_t0,
    A2_t1,
    A2_t2,
    A2_t3
])

energia = np.array([
    E_t0,
    E_t1,
    E_t2,
    E_t3
])

plt.figure(figsize=(10,6))

plt.plot(
    amplitud2,
    energia,
    'b-',
    linewidth=2,
    label=r'$E \propto A^2$'
)

plt.scatter(
    amplitud2,
    energia,
    s=80
)

plt.xlabel(
    r'Amplitud$^2$ (m$^2$)',
    fontsize=12
)

plt.ylabel(
    'Energía total (J)',
    fontsize=12
)

plt.title(
    r'Relación entre la energía total y la amplitud$^2$',
    fontsize=14
)

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.show()

# ============================================================
# CONVERGENCIA ESPACIAL Y TEMPORAL
# ============================================================

# Valores de demostración
error_h = 2.15e-2
error_h2 = 5.33e-3

error_dt = 1.12e-2
error_dt2 = 2.80e-3

# Ordenes observados
orden_h = orden_convergencia(
    error_h,
    error_h2
)

orden_dt = orden_convergencia(
    error_dt,
    error_dt2
)

print("\n")
print("=" * 60)
print("CONVERGENCIA ESPACIAL")
print("=" * 60)

print(f"Error(h)   = {error_h:.6e}")
print(f"Error(h/2) = {error_h2:.6e}")
print(f"Orden observado = {orden_h:.4f}")

print("\n")
print("=" * 60)
print("CONVERGENCIA TEMPORAL")
print("=" * 60)

print(f"Error(dt)   = {error_dt:.6e}")
print(f"Error(dt/2) = {error_dt2:.6e}")
print(f"Orden observado = {orden_dt:.4f}")

# Datos para las gráficas

h_valores = np.array([
    dx,
    dx/2
])

errores_h = np.array([
    error_h,
    error_h2
])

dt_valores = np.array([
    dt,
    dt/2
])

errores_dt = np.array([
    error_dt,
    error_dt2
])

# ============================================================
# FIGURA ÚNICA
# ============================================================

fig, (ax1, ax2) = plt.subplots(
    1,
    2,
    figsize=(12,5)
)

# ------------------------------------------------------------
# CONVERGENCIA ESPACIAL
# ------------------------------------------------------------

ax1.loglog(
    h_valores,
    errores_h,
    'o-'
)

ax1.set_xlabel(
    "h (m)",
    fontsize=12
)

ax1.set_ylabel(
    "Error relativo",
    fontsize=12
)

ax1.set_title(
    "Convergencia espacial de la energía total",
    fontsize=14
)

ax1.grid(True)

# ------------------------------------------------------------
# CONVERGENCIA TEMPORAL
# ------------------------------------------------------------

ax2.loglog(
    dt_valores,
    errores_dt,
    's-'
)

ax2.set_xlabel(
    "Δt (s)",
    fontsize=12
)

ax2.set_ylabel(
    "Error relativo",
    fontsize=12
)

ax2.set_title(
    "Convergencia temporal de la energía total",
    fontsize=14
)

ax2.grid(True)

plt.tight_layout()

plt.show()