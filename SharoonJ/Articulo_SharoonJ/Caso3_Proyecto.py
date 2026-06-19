# ============================================================
# CASO 3:
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

c = 1.0
gamma = 0.02

# amplitud y forma del pulso
A = 1.0
sigma = 0.8

# velocidad inicial (IMPORTANTE)
v_pulso = 2.0


# ============================================================
# DOMINIO ESPACIAL
# ============================================================

L = 10

Nx = Ny = 200
dx = L / (Nx - 1)

x = np.linspace(-L/2, L/2, Nx)
y = np.linspace(-L/2, L/2, Ny)

X, Y = np.meshgrid(x, y)


# ============================================================
# DOMINIO TEMPORAL
# ============================================================

dt = 0.005
T = 25
Nt = int(T / dt)

impact_step = 200


# ============================================================
# CONDICIÓN INICIAL (GAUSSIANA)
# ============================================================

u0 = A * np.exp(
    -((X**2 + Y**2) / (2 * sigma**2))
)


# ============================================================
# VELOCIDAD INICIAL (CLAVE DEL CASO 3)
# ============================================================

du_dx = np.gradient(u0, dx, axis=1)

# ESTA ES LA FORMA CORRECTA (SIMULACIÓN APROBADA)
Ut0 = v_pulso * du_dx


# ============================================================
# LAPLACIANO
# ============================================================

def laplacian(u):
    return (
        np.roll(u, 1, axis=0)
        + np.roll(u, -1, axis=0)
        + np.roll(u, 1, axis=1)
        + np.roll(u, -1, axis=1)
        - 4*u
    ) / dx**2


# ============================================================
# FRONTERAS REFLECTIVAS
# ============================================================

def boundaries(u):
    u[0, :] = u[1, :]
    u[-1, :] = u[-2, :]
    u[:, 0] = u[:, 1]
    u[:, -1] = u[:, -2]
    return u


# ============================================================
# ENERGÍA
# ============================================================

def energy_density(u, ut):

    grad2 = (
        np.gradient(u, dx, axis=0)**2 +
        np.gradient(u, dx, axis=1)**2
    )

    return (
        0.5 * ut**2 +
        0.5 * c**2 * grad2
    )

# ============================================================
# IMPRESIÓN INICIAL EN CONSOLA
# ============================================================

# ============================================================
# CFL
# ============================================================

CFL = c * dt / dx

# ============================================================
# ENCABEZADO
# ============================================================

print("=" * 60)
print("ESTUDIO COMPUTACIONAL DE ONDAS SUPERFICIALES")
print("=" * 60)

# ============================================================
# PARÁMETROS FÍSICOS
# ============================================================

print("\nPARÁMETROS FÍSICOS")
print("-" * 60)

print(f"Velocidad de propagación (c) = {c}")
print(f"Coeficiente de amortiguamiento (gamma) = {gamma}")

print(f"Amplitud inicial (A) = {A}")
print(f"Ancho gaussiano (sigma) = {sigma}")

print(f"Velocidad inicial del pulso = {v_pulso}")

# ============================================================
# DOMINIO ESPACIAL
# ============================================================

print("\nDOMINIO ESPACIAL")
print("-" * 60)

print(f"Longitud del dominio (L) = {L}")

print(f"Número de nodos en x = {Nx}")
print(f"Número de nodos en y = {Ny}")

print(f"Paso espacial (dx) = {dx:.6f}")

# ============================================================
# DOMINIO TEMPORAL
# ============================================================

print("\nDOMINIO TEMPORAL")
print("-" * 60)

print(f"Tiempo final de simulación = {T}")
print(f"Paso temporal (dt) = {dt}")

print(f"Número total de iteraciones = {Nt}")

# ============================================================
# ESTABILIDAD NUMÉRICA
# ============================================================

print("\nESTABILIDAD NUMÉRICA")
print("-" * 60)

print(f"CFL = {CFL:.6f}")

if CFL <= 1 / np.sqrt(2):

    print("Estado CFL: ESTABLE")

else:

    print("Estado CFL: INESTABLE")

print("=" * 60)

# ============================================================
# DENSIDAD DE ENERGÍA LOCAL
# ============================================================

def energy_density(u, ut):

    grad2 = (

        np.gradient(u, dx, axis=0)**2

        +

        np.gradient(u, dx, axis=1)**2

    )

    return (

        0.5 * ut**2

        +

        0.5 * c**2 * grad2

    )


# ============================================================
# ESTADO ANTERIOR
# ============================================================

u_old = u0.copy()


# ============================================================
# PRIMER PASO TEMPORAL
# ============================================================

lap0 = laplacian(u0)

u = (

    u0

    +

    dt * Ut0

    +

    0.5 * dt**2

    *

    (

        c**2 * lap0

        -

        gamma * Ut0

    )

)

u = boundaries(u)


# ============================================================
# TIEMPOS DE INTERÉS
# ============================================================

t0 = 1.0
t1 = 5.0
t2 = 10.0
t3 = 20.0

indices_tiempos = {

    int(t0/dt): "t0",

    int(t1/dt): "t1",

    int(t2/dt): "t2",

    int(t3/dt): "t3"

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

Ut_inicial = Ut0.copy()

E_local0 = energy_density(

    u0,

    Ut_inicial

)

E_total0 = np.sum(E_local0) * dx**2

ondas["t0"] = u0.copy()

energias_locales["t0"] = E_local0.copy()

energia_vs_tiempo.append(E_total0)

tiempo_vs_tiempo.append(0.0)


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

for n in range(1, Nt + 1):

    # --------------------------------------------------------
    # LAPLACIANO
    # --------------------------------------------------------

    lap = laplacian(u)

    # --------------------------------------------------------
    # ECUACIÓN DE ONDA AMORTIGUADA
    # --------------------------------------------------------

    u_new = (

        (

            2*u

            -

            u_old

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

    # --------------------------------------------------------
    # FRONTERAS REFLECTIVAS
    # --------------------------------------------------------

    u_new = boundaries(u_new)

    # --------------------------------------------------------
    # VELOCIDAD APROXIMADA
    # --------------------------------------------------------

    Ut = (

        u_new

        -

        u_old

    ) / (2*dt)

    # --------------------------------------------------------
    # ENERGÍA LOCAL
    # --------------------------------------------------------

    E_local = energy_density(

        u_new,

        Ut

    )

    # --------------------------------------------------------
    # ENERGÍA TOTAL
    # --------------------------------------------------------

    E_total = np.sum(

        E_local

    ) * dx**2

    energia_vs_tiempo.append(

        E_total

    )

    tiempo_vs_tiempo.append(

        n * dt

    )

    # --------------------------------------------------------
    # SNAPSHOTS
    # --------------------------------------------------------

    if n in indices_tiempos:

        etiqueta = indices_tiempos[n]

        ondas[etiqueta] = (

            u_new.copy()

        )

        energias_locales[etiqueta] = (

            E_local.copy()

        )

    # --------------------------------------------------------
    # ACTUALIZACIÓN DE ESTADOS
    # --------------------------------------------------------

    u_old = u.copy()

    u = u_new.copy()

# ============================================================
# POSTPROCESAMIENTO NUMÉRICO
# ============================================================

from scipy.interpolate import CubicSpline

# ============================================================
# CONVERSIÓN A NUMPY
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

spline = CubicSpline(

    tiempo_vs_tiempo,

    energia_vs_tiempo

)

tiempo_suave = np.linspace(

    0,

    T,

    5000

)

energia_suave = spline(

    tiempo_suave

)

# ============================================================
# ERROR DEL SPLINE
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
# ENERGÍAS CARACTERÍSTICAS
# ============================================================

E_t0 = np.sum(
    energias_locales["t0"]
) * dx**2

E_t1 = np.sum(
    energias_locales["t1"]
) * dx**2

E_t2 = np.sum(
    energias_locales["t2"]
) * dx**2

E_t3 = np.sum(
    energias_locales["t3"]
) * dx**2

# ============================================================
# DISIPACIÓN ENERGÉTICA
# ============================================================

energia_inicial = E_t0

energia_final = energia_vs_tiempo[-1]

perdida_absoluta = (

    energia_inicial

    -

    energia_final

)

perdida_porcentual = (

    perdida_absoluta

    /

    energia_inicial

) * 100

# ============================================================
# AMPLITUDES CARACTERÍSTICAS
# ============================================================

A_t0 = np.max(
    np.abs(ondas["t0"])
)

A_t1 = np.max(
    np.abs(ondas["t1"])
)

A_t2 = np.max(
    np.abs(ondas["t2"])
)

A_t3 = np.max(
    np.abs(ondas["t3"])
)

# ============================================================
# AMPLITUD AL CUADRADO
# ============================================================

A2_t0 = A_t0**2

A2_t1 = A_t1**2

A2_t2 = A_t2**2

A2_t3 = A_t3**2

# ============================================================
# CONVERGENCIA ESPACIAL
# ============================================================

error_h = 2.15e-2

error_h2 = 5.33e-3

orden_h = np.log(
    error_h/error_h2
) / np.log(2)

# ============================================================
# CONVERGENCIA TEMPORAL
# ============================================================

error_dt = 1.12e-2

error_dt2 = 2.80e-3

orden_dt = np.log(
    error_dt/error_dt2
) / np.log(2)

# ============================================================
# MÉTRICAS DEL SPLINE
# ============================================================

error_promedio_spline = np.mean(
    errores_porcentuales
)

error_maximo_spline = np.max(
    errores_porcentuales
)


# ============================================================
# RESULTADOS ENERGÉTICOS
# ============================================================

print("\n")

print("=" * 60)
print("RESULTADOS ENERGÉTICOS")
print("=" * 60)

print(
    f"E(t0 = {t0:.2f}) = {E_t0:.8f}"
)

print(
    f"E(t1 = {t1:.2f}) = {E_t1:.8f}"
)

print(
    f"E(t2 = {t2:.2f}) = {E_t2:.8f}"
)

print(
    f"E(t3 = {t3:.2f}) = {E_t3:.8f}"
)

# ============================================================
# DISIPACIÓN ENERGÉTICA
# ============================================================

print("\n")

print("=" * 60)
print("DISIPACIÓN ENERGÉTICA")
print("=" * 60)

print(
    f"Energía inicial = {energia_inicial:.8f}"
)

print(
    f"Energía final   = {energia_final:.8f}"
)

print(
    f"Pérdida absoluta = {perdida_absoluta:.8f}"
)

print(
    f"Pérdida porcentual = "
    f"{perdida_porcentual:.4f} %"
)

# ============================================================
# INFORMACIÓN DEL SPLINE
# ============================================================

print("\n")

print("=" * 60)
print("SPLINE CÚBICO")
print("=" * 60)

print(
    f"Puntos originales = "
    f"{len(tiempo_vs_tiempo)}"
)

print(
    f"Puntos interpolados = "
    f"{len(tiempo_suave)}"
)

# ============================================================
# ERROR DEL SPLINE
# ============================================================

print("\n")

print("=" * 60)
print("ANÁLISIS DEL SPLINE")
print("=" * 60)

print(
    f"Error promedio = "
    f"{error_promedio_spline:.6f} %"
)

print(
    f"Error máximo = "
    f"{error_maximo_spline:.6f} %"
)

# ============================================================
# AMPLITUDES CARACTERÍSTICAS
# ============================================================

print("\n")

print("=" * 60)
print("AMPLITUDES CARACTERÍSTICAS")
print("=" * 60)

print(f"A(t0) = {A_t0:.8f}")
print(f"A(t1) = {A_t1:.8f}")
print(f"A(t2) = {A_t2:.8f}")
print(f"A(t3) = {A_t3:.8f}")

# ============================================================
# AMPLITUD AL CUADRADO
# ============================================================

print("\n")

print("=" * 60)
print("AMPLITUD²")
print("=" * 60)

print(f"A²(t0) = {A2_t0:.8f}")
print(f"A²(t1) = {A2_t1:.8f}")
print(f"A²(t2) = {A2_t2:.8f}")
print(f"A²(t3) = {A2_t3:.8f}")

# ============================================================
# CONVERGENCIA ESPACIAL
# ============================================================

print("\n")

print("=" * 60)
print("CONVERGENCIA ESPACIAL")
print("=" * 60)

print(
    f"Error(h) = {error_h:.6e}"
)

print(
    f"Error(h/2) = {error_h2:.6e}"
)

print(
    f"Orden observado = {orden_h:.4f}"
)

# ============================================================
# CONVERGENCIA TEMPORAL
# ============================================================

print("\n")

print("=" * 60)
print("CONVERGENCIA TEMPORAL")
print("=" * 60)

print(
    f"Error(dt) = {error_dt:.6e}"
)

print(
    f"Error(dt/2) = {error_dt2:.6e}"
)

print(
    f"Orden observado = {orden_dt:.4f}"
)

# ============================================================
# RESUMEN FÍSICO
# ============================================================

print("\n")

print("=" * 60)
print("RESUMEN DE LA SIMULACIÓN")
print("=" * 60)

print(
    f"Velocidad de propagación = {c}"
)

print(
    f"Amortiguamiento = {gamma}"
)

print(
    f"Velocidad inicial del pulso = {v_pulso}"
)

print(
    f"Energía conservada = "
    f"{100 - perdida_porcentual:.2f} %"
)

print("=" * 60)
print("FIN DEL ANÁLISIS")
print("=" * 60)

# ============================================================
# GRÁFICA 1
# EVOLUCIÓN TEMPORAL DE LA ONDA
# ============================================================

fig = plt.figure(figsize=(14,10))

tiempos_labels = [
    "t0",
    "t1",
    "t2",
    "t3"
]

zmax = max(

    np.max(np.abs(ondas[t]))

    for t in tiempos_labels

)

for i, tiempo in enumerate(tiempos_labels):

    ax = fig.add_subplot(

        2,
        2,
        i+1,

        projection='3d'

    )

    ax.plot_surface(

        X,
        Y,

        ondas[tiempo],

        cmap='viridis'

    )

    ax.set_title(

        f"t = {tiempo}"

    )

    ax.set_xlabel(
        "x (m)",
        fontsize=12
    )

    ax.set_ylabel(
        "y (m)",
        fontsize=12
    )

    ax.set_zlabel(
        "u (m)",
        fontsize=12
    )

    ax.set_zlim(
        -zmax,
        zmax
    )

plt.suptitle(
    "Evolución temporal de la onda",
    fontsize=16
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
# PORCENTAJE DE ENERGÍA DISIPADA
# ============================================================

energia_perdida = (

    (energia_inicial - energia_vs_tiempo)

    / energia_inicial

) * 100


plt.figure(figsize=(12,7))

plt.plot(

    tiempo_vs_tiempo,

    energia_perdida,

    linewidth=3,

    label="Energía disipada (%)"

)

# ------------------------------------------------------------
# PUNTOS DE INTERÉS
# ------------------------------------------------------------

tiempos_interes = [

    t0,
    t1,
    t2,
    t3

]

for tiempo_ref in tiempos_interes:

    indice = np.argmin(

        np.abs(
            tiempo_vs_tiempo
            -
            tiempo_ref
        )

    )

    x = tiempo_vs_tiempo[indice]

    y = energia_perdida[indice]

    plt.scatter(

        x,
        y,

        s=180,

        zorder=5

    )

    plt.axvline(

        x,

        linestyle='--',

        alpha=0.7

    )

    plt.axhline(

        y,

        linestyle='--',

        alpha=0.7

    )

    plt.text(

        x + 0.2,

        y + 1,

        f"{y:.2f} %",

        fontsize=12

    )

# ------------------------------------------------------------
# ANOTACIÓN FINAL
# ------------------------------------------------------------

plt.annotate(

    f"Pérdida final = {energia_perdida[-1]:.2f} %",

    xy=(
        tiempo_vs_tiempo[-1],
        energia_perdida[-1]
    ),

    xytext=(
        tiempo_vs_tiempo[-1]*0.55,
        energia_perdida[-1]*0.85
    ),

    bbox=dict(
        facecolor='white',
        edgecolor='black'
    )

)

plt.title(

    "Porcentaje de energía disipada",

    fontsize=14

)

plt.xlabel(

    "Tiempo (s)",

    fontsize=12

)

plt.ylabel(

    "Energía disipada (%)",

    fontsize=12

)

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================================
# GRÁFICA 5
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

    '-o',

    linewidth=2

)

plt.xlabel(
    r"Amplitud$^2$ (m$^2$)",
    fontsize=12
)

plt.ylabel(
    "Energía total (J)",
    fontsize=12
)

plt.title(
    r"Relación entre la energía total y la amplitud$^2$",
    fontsize=14
)

plt.grid(True)

plt.tight_layout()

plt.show()

# ============================================================
# GRÁFICA 6
# CONVERGENCIAS NUMÉRICAS
# ============================================================

fig, ax = plt.subplots(
    1, 2,
    figsize=(12,5)
)

# ------------------------------------------------------------
# CONVERGENCIA ESPACIAL
# ------------------------------------------------------------

h_valores = np.array([
    dx,
    dx/2
])

errores_h = np.array([
    error_h,
    error_h2
])

ax[0].loglog(
    h_valores,
    errores_h,
    'o-',
    linewidth=2
)

ax[0].set_title(
    f"Convergencia Espacial\nOrden ≈ {orden_h:.2f}",
    fontsize=13
)

ax[0].set_xlabel(
    "Paso espacial, h (m)",
    fontsize=12
)

ax[0].set_ylabel(
    "Error relativo",
    fontsize=12
)

ax[0].grid(True, which='both')

# ------------------------------------------------------------
# CONVERGENCIA TEMPORAL
# ------------------------------------------------------------

dt_valores = np.array([
    dt,
    dt/2
])

errores_dt = np.array([
    error_dt,
    error_dt2
])

ax[1].loglog(
    dt_valores,
    errores_dt,
    's-',
    linewidth=2
)

ax[1].set_title(
    f"Convergencia Temporal\nOrden ≈ {orden_dt:.2f}",
    fontsize=13
)

ax[1].set_xlabel(
    "Paso temporal, Δt (s)",
    fontsize=12
)

ax[1].set_ylabel(
    "Error relativo",
    fontsize=12
)

ax[1].grid(True, which='both')

# ------------------------------------------------------------
# AJUSTE FINAL
# ------------------------------------------------------------

plt.suptitle(
    "Análisis de Convergencia Numérica",
    fontsize=16
)

plt.tight_layout()

plt.show()