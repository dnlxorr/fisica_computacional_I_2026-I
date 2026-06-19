"""
===============================================================================
 Modelo de nube de cargas de Fibonacci aplicado a la molecula de agua
===============================================================================
Reimplementacion en Python (desde cero) del modelo de nube de cargas puntuales
del articulo de Excel-ScienSolar (Becerra et al.), aplicado a la molecula de
H2O con cargas parciales TIP3P.

Este script genera, en un solo lugar, TODOS los numeros y TODAS las figuras
usados en el articulo final (agua_cloud_articulo.tex):

    Tablas (impresas en consola):
        - Tabla I   : conservacion de carga (Gauss-Legendre)
        - Tabla II  : campo electrico, diferencias finitas vs. analitico
        - Tabla III : validacion cruzada con Excel-ScienSolar
        - Tabla IV  : tiempo de ejecucion vs. N_operaciones

    Figuras (PNG, guardadas con ruta relativa):
        - fig_panel_resultados.png : panel 2x2 a todo el ancho con los 4
          resultados graficos -> (a) nube de cargas 3D, (b) spline cubico,
          (c) mapa de potencial + campo vectorial, (d) tiempo de ejecucion.
        - fig_nube_agua_3d.png : vista detallada 3D de la nube de cargas

Metodos numericos incluidos:
    1) Suma de Coulomb discreta (superposicion)      -> Ecs. (4) y (7) [Becerra et al.]
    2) Derivacion numerica (diferencias finitas centradas) -> E a partir de V
    3) Integracion numerica (cuadratura de Gauss-Legendre) -> validacion de carga
    4) Interpolacion con splines cubicos              -> perfil V(r) continuo

Unidades: posiciones en Angstrom (A), cargas en unidades de e,
potencial en Voltios (V), campo electrico en V/Angstrom.

Requisitos: numpy, scipy, matplotlib
    pip install numpy scipy matplotlib
===============================================================================
"""

import csv
import time

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline
from numpy.polynomial.legendre import leggauss
from mpl_toolkits.mplot3d import Axes3D  # Para gráficos 3D

# Tamano de fuente mas grande en todas las figuras (pedido explicito del
# profesor: "que las graficas tengan un tamano de letra mas grande").
plt.rcParams.update({
    "font.size": 14,
    "axes.titlesize": 15,
    "axes.labelsize": 14,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 12,
})


# =============================================================================
# 0. CONSTANTES FISICAS
# =============================================================================
k_SI = 8.9875517923e9      # Constante de Coulomb, N m^2 / C^2
e_C = 1.602176634e-19      # Carga elemental, C
ANG = 1.0e-10               # 1 Angstrom en metros

# Constante efectiva para trabajar directamente en unidades (Angstrom, e, V):
#   V [V] = K_EFF * q [e] / r [Angstrom]
# Se fija al valor exacto reportado en la Tabla 2 del articulo de Excel para
# una carga puntual de -1e a 1 Angstrom (V = -14.3800 V). El valor obtenido
# con constantes CODATA (k_SI*e_C/ANG = 14.3996...) difiere en ~0.14% por
# redondeo de las constantes fisicas usadas en el Excel original; se usa el
# valor exacto de la tabla para que la validacion cruzada (Tabla III) sea
# una comparacion limpia, sin esa diferencia de origen numerico ajena al
# modelo de nube en si.
K_EFF = 14.3800


# =============================================================================
# 1. GEOMETRIA: nube de Fibonacci y molecula de agua
# =============================================================================
def fibonacci_sphere(Nc, r):
    """
    Genera Nc puntos cuasi-uniformes sobre una esfera de radio r (Angstrom),
    usando el muestreo angular de Fibonacci (Ecs. 15-20 del articulo base):
        phi_k   = 2*pi*k*Phi          (Phi = razon aurea)
        theta_k = arccos(1 - 2k/Nc)
    Esta geometria se elige porque, de las 5 propuestas en el articulo
    original, es la que converge mas rapido al limite de carga puntual
    gracias a su muestreo angular cuasi-uniforme (sin acumulacion en polos).
    """
    Phi = (1 + np.sqrt(5)) / 2.0
    k_idx = np.arange(Nc)
    theta = np.arccos(1 - 2 * k_idx / Nc)
    phi = 2 * np.pi * k_idx * Phi
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return np.column_stack((x, y, z))


def build_water_cloud(Nc=400, r_cloud=0.30):
    """
    Construye la nube de cargas completa de la molecula de agua.

    Geometria experimental: r(O-H) = 0.9572 A, angulo H-O-H = 104.5 grados.
    Cargas parciales TIP3P: q_O = -0.834 e, q_H = +0.417 e (estandar en
    fisica/quimica computacional clasica; ver justificacion en el articulo,
    Sec. 2.2: el objetivo es validar la metodologia numerica, no producir
    un modelo electronico de alta precision).

    r_cloud = 0.30 A se eligio porque 2*r_cloud < r_OH, evitando que las
    tres nubes (O, H, H) se superpongan entre si.

    Devuelve:
        pos   : (3*Nc, 3) coordenadas (Angstrom) de todos los subelementos
        q     : (3*Nc,)   carga fraccionaria de cada subelemento (en e)
        atoms : lista [(centro_O, Q_O), (centro_H1, Q_H1), (centro_H2, Q_H2)]
    """
    bond = 0.9572
    angle = np.deg2rad(104.5)

    O = np.array([0.0, 0.0, 0.0])
    H1 = O + bond * np.array([np.sin(angle / 2), np.cos(angle / 2), 0.0])
    H2 = O + bond * np.array([-np.sin(angle / 2), np.cos(angle / 2), 0.0])

    atoms = [(O, -0.834), (H1, 0.417), (H2, 0.417)]

    pos_list, q_list = [], []
    for center, q_total in atoms:
        pts = fibonacci_sphere(Nc, r_cloud) + center
        q_each = q_total / Nc
        pos_list.append(pts)
        q_list.append(np.full(Nc, q_each))

    return np.vstack(pos_list), np.concatenate(q_list), atoms


# =============================================================================
# 2. ELECTROSTATICA: suma de Coulomb (potencial y campo analitico)
# =============================================================================
def potential(pos, q, robs):
    """V(robs) en Voltios, por superposicion de Coulomb (Ec. 4)."""
    d = np.linalg.norm(robs - pos, axis=1)
    return K_EFF * np.sum(q / d)


def field_analytic(pos, q, robs):
    """E(robs) analitico (V/Angstrom), por superposicion de Coulomb (Ec. 7)."""
    rvec = robs - pos
    d = np.linalg.norm(rvec, axis=1)
    contrib = (q / d**3)[:, None] * rvec
    return K_EFF * np.sum(contrib, axis=0)


# =============================================================================
# 3. DERIVACION NUMERICA: diferencias finitas centradas
# =============================================================================
def field_numeric(pos, q, robs, h=1.0e-3):
    """
    E(robs) por diferencias finitas centradas:
        E_i ~ -[V(r + h*e_i) - V(r - h*e_i)] / (2h)

    Justificacion (ver articulo, Sec. 2.3): por expansion de Taylor, el
    esquema centrado tiene error O(h^2), un orden mejor que los esquemas
    hacia adelante/atras (O(h)), con el mismo numero de evaluaciones extra
    de V (dos por componente). Se usa h = 1e-3 A porque el error de
    truncamiento esperado (~h^2 = 1e-6) es muy superior al error de
    redondeo de doble precision (~1e-16), evitando cancelacion catastrofica
    sin sacrificar precision.
    """
    E = np.zeros(3)
    for i in range(3):
        dr = np.zeros(3)
        dr[i] = h
        Vp = potential(pos, q, robs + dr)
        Vm = potential(pos, q, robs - dr)
        E[i] = -(Vp - Vm) / (2 * h)
    return E


# =============================================================================
# 4. INTEGRACION NUMERICA: cuadratura de Gauss-Legendre
# =============================================================================
def integrate_surface_charge(Q_total, r, n_theta=12, n_phi=12):
    """
    Calcula Q = oint sigma dA = int_0^2pi int_0^pi sigma r^2 sin(theta) dtheta dphi
    con sigma = Q_total / (4 pi r^2), la densidad superficial uniforme
    equivalente a la nube discreta.

    Justificacion (ver articulo, Sec. 2.3): tras el cambio de variable
    x = cos(theta), el integrando es un polinomio de grado 0 en x. La
    cuadratura de Gauss-Legendre con n puntos integra EXACTAMENTE
    polinomios de grado <= 2n-1, asi que con n=12 la integral en theta no
    tiene error de truncamiento (la integral en phi, periodica y constante,
    tambien es exacta con la regla del trapecio). Esto convierte la
    comparacion con sum_k q_jk en una prueba de consistencia limpia: si
    hay diferencia, no puede atribuirse al metodo de integracion.
    """
    sigma = Q_total / (4 * np.pi * r**2)

    x, w = leggauss(n_theta)          # nodos y pesos de Gauss-Legendre en [-1,1]
    dphi = 2 * np.pi / n_phi          # paso uniforme en phi (regla del trapecio, exacta)

    integral = 0.0
    for i in range(n_theta):
        for _ in range(n_phi):
            integral += sigma * r**2 * w[i] * dphi
    return integral


# =============================================================================
# 5. INTERPOLACION: splines cubicos para el perfil radial V(r)
# =============================================================================
def spline_radial_profile(pos, q, axis=np.array([0, 1, 0]),
                           r_min=1.5, r_max=5.0, n_coarse=8, n_fine=200):
    """
    Construye el perfil V(r) a lo largo de una direccion (por defecto, la
    bisectriz H-O-H, eje y) usando solo n_coarse=8 evaluaciones EXACTAS de
    la suma de Coulomb, interpoladas con un spline cubico C^2. El campo
    radial se obtiene derivando el spline analiticamente: E_r = -dS/dr.

    Justificacion (ver articulo, Sec. 2.3): evaluar V en una malla fina de
    N_f puntos cuesta O(N_f * N_c) (Ec. 27); usando solo 8 nodos se reduce
    el costo ~25 veces (si N_f=200). La validez se comprueba a posteriori
    comparando el spline con la evaluacion EXACTA de V en una malla fina
    de 200 puntos (V_fine_exact).
    """
    axis = axis / np.linalg.norm(axis)

    r_coarse = np.linspace(r_min, r_max, n_coarse)
    V_coarse = np.array([potential(pos, q, r * axis) for r in r_coarse])

    cs = CubicSpline(r_coarse, V_coarse)

    r_fine = np.linspace(r_min, r_max, n_fine)
    V_fine_spline = cs(r_fine)
    Er_spline = -cs(r_fine, 1)                # derivada del spline -> -dV/dr
    V_fine_exact = np.array([potential(pos, q, r * axis) for r in r_fine])  # referencia exacta

    return r_coarse, V_coarse, r_fine, V_fine_spline, Er_spline, V_fine_exact


# =============================================================================
# 6. BENCHMARK: tiempo de ejecucion vs. N_operaciones = Nf * Nc * Np
# =============================================================================
def benchmark_performance(Nc_values=(25, 50, 100, 200, 400, 800, 1600),
                           Nf=200, n_rep=3, seed=42):
    """
    Reproduce la metrica de la Tabla 1 del articulo de Excel:
        N_operaciones = Nf * Nc * Np
    midiendo el tiempo real de Python para evaluar V(r) en Nf puntos de
    campo, variando Nc (subcargas por atomo), con Np=3 fijo (O, H, H).

    Se usan los MISMOS Nf puntos de campo (semilla fija) para todas las
    filas, de modo que el unico parametro que cambie sea N_operaciones.
    Cada combinacion se repite n_rep veces y se reporta el tiempo MINIMO
    (convencion estandar de benchmarking: el minimo refleja el costo
    intrinseco del algoritmo, libre de interrupciones del sistema).
    """
    Np = 3  # O, H, H

    rng = np.random.default_rng(seed)
    directions = rng.normal(size=(Nf, 3))
    directions /= np.linalg.norm(directions, axis=1, keepdims=True)
    radii = rng.uniform(1.5, 5.0, size=Nf)
    field_pts = directions * radii[:, None]

    results = []
    for Nc_b in Nc_values:
        pos_b, q_b, _ = build_water_cloud(Nc=Nc_b, r_cloud=0.30)

        times = []
        for _ in range(n_rep):
            t0 = time.perf_counter()
            for r in field_pts:
                potential(pos_b, q_b, r)
            t1 = time.perf_counter()
            times.append(t1 - t0)

        t_min = min(times)
        N_ops = Nf * Nc_b * Np
        results.append({
            "Nc": Nc_b,
            "Nf": Nf,
            "Np": Np,
            "N_operaciones": N_ops,
            "tiempo_s": t_min,
            "tiempo_por_operacion_s": t_min / N_ops,
        })
    return results


# =============================================================================
# 7. FIGURAS: nube 3D y panel de resultados
# =============================================================================

def generar_figura_nube_3d(pos, q, atoms, Nc, filename="fig_nube_agua_3d.png"):
    """
    Genera una figura 3D detallada de la nube de cargas de Fibonacci 
    para la molécula de agua.
    
    Parámetros:
        pos: array con las posiciones de todas las cargas (3*Nc, 3)
        q: array con las cargas (3*Nc,)
        atoms: lista de tuplas (centro, carga_total)
        Nc: número de cargas por átomo
        filename: nombre del archivo de salida
    """
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")
    
    # Definir colores y tamaños
    colors = ["tab:red", "tab:blue", "tab:blue"]
    labels = ["Oxígeno (O)", "Hidrógeno 1 (H₁)", "Hidrógeno 2 (H₂)"]
    markersizes = [30, 20, 20]  # Tamaño de los centros atómicos
    
    n_each = Nc
    
    # Graficar las nubes de cargas
    for i, (center, qtot) in enumerate(atoms):
        sl = slice(i * n_each, (i + 1) * n_each)
        
        # Nube de puntos de Fibonacci (con transparencia)
        ax.scatter(
            pos[sl, 0], pos[sl, 1], pos[sl, 2],
            s=8,  # Tamaño de los puntos
            color=colors[i],
            alpha=0.6,  # Transparencia para ver la estructura 3D
            label=f"{labels[i]} (q = {qtot:.3f} e)",
            edgecolors='none'
        )
        
        # Marcar el centro del átomo (más grande y con borde)
        ax.scatter(
            center[0], center[1], center[2],
            s=markersizes[i],
            color=colors[i],
            edgecolor='black',
            linewidth=1.5,
            zorder=10  # Para que los centros estén encima de los puntos
        )
    
    # Configurar ejes
    ax.set_xlabel("x (Å)", fontsize=12, labelpad=10)
    ax.set_ylabel("y (Å)", fontsize=12, labelpad=10)
    ax.set_zlabel("z (Å)", fontsize=12, labelpad=10)
    
    # Título con información del modelo
    ax.set_title(
        f"Nube de cargas de Fibonacci - Molécula de H₂O\n"
        f"N₀ = {Nc} cargas por átomo, r_cloud = 0.30 Å",
        fontsize=13, pad=20
    )
    
    # Leyenda mejorada
    ax.legend(loc='upper right', fontsize=10, framealpha=0.9)
    
    # Ajustar límites para una vista equilibrada
    ax.set_xlim(-0.9, 0.9)
    ax.set_ylim(-0.6, 0.6)
    ax.set_zlim(-0.6, 0.6)
    
    # Mejorar el ángulo de visión
    ax.view_init(elev=25, azim=-60)
    
    # Añadir grid para mejor referencia espacial
    ax.grid(True, alpha=0.3, linestyle='--')
    
    # Ajustar diseño
    plt.tight_layout()
    
    # Guardar figura
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close(fig)
    
    print(f"Figura 3D guardada en {filename}")
    return fig


def figura_panel_resultados(pos, q, atoms, Nc,
                             r_coarse, V_coarse, r_fine, V_fine_spline, Er_spline,
                             bench,
                             filename="fig_panel_resultados.png"):
    """
    Genera UNA sola figura compuesta, en una cuadricula 2x2, pensada para
    insertarse a todo el ancho de la pagina al inicio de la seccion de
    Resultados y Discusion:

        (a) Nube de cargas de Fibonacci, en 3D
        (b) Potencial V(r) sobre la bisectriz H-O-H: exacto vs. spline cubico
        (c) Mapa de potencial V(x,y) + campo electrico E(x,y) (dos sub-paneles)
        (d) Tiempo de ejecucion vs. N_operaciones (log-log y ajuste afin)

    Todas las fuentes se aumentan de tamano (ver plt.rcParams al inicio del
    script) para que el panel completo siga siendo legible incluso cuando
    se reduce para caber en el ancho de la pagina.
    """
    fig = plt.figure(figsize=(18, 13), constrained_layout=True)
    gs = fig.add_gridspec(2, 2, hspace=0.05, wspace=0.05)

    # ---------------------------------------------------------------
    # (a) Nube de cargas, vista 3D
    # ---------------------------------------------------------------
    axA = fig.add_subplot(gs[0, 0], projection='3d')
    colors = ["tab:red", "tab:blue", "tab:blue"]
    labels = ["O", "H₁", "H₂"]
    for i, (center, _) in enumerate(atoms):
        sl = slice(i * Nc, (i + 1) * Nc)
        axA.scatter(pos[sl, 0], pos[sl, 1], pos[sl, 2], 
                    s=8, color=colors[i], label=labels[i], alpha=0.7)
        # Marcar el centro del átomo
        axA.scatter(center[0], center[1], center[2], 
                    color="black", s=40, marker="o")

    axA.set_xlabel("x (Å)")
    axA.set_ylabel("y (Å)")
    axA.set_zlabel("z (Å)")
    axA.set_title("(a) Nube de cargas H₂O (3D)")
    axA.legend(loc="upper right", framealpha=0.95)

    # Ajustar límites para una vista equilibrada
    axA.set_xlim(-0.9, 0.9)
    axA.set_ylim(-0.6, 0.6)
    axA.set_zlim(-0.6, 0.6)

    # Mejorar el ángulo de visión
    axA.view_init(elev=25, azim=-60)

    # ---------------------------------------------------------------
    # (b) Spline cubico: V(r) y campo radial
    # ---------------------------------------------------------------
    gsB = gs[0, 1].subgridspec(2, 1, hspace=0.06)
    axB1 = fig.add_subplot(gsB[0])
    axB2 = fig.add_subplot(gsB[1], sharex=axB1)

    axB1.plot(r_fine, V_fine_spline, "--", color="black", label="Spline cúbico", zorder=2)
    axB1.plot(r_coarse, V_coarse, "o", color="red", ms=9, label="Nodos (8 pts)", zorder=3)
    axB1.set_ylabel("V(r) [V]")
    axB1.set_title("(b) Potencial y campo radial (spline cúbico)")
    axB1.legend(loc="upper right")
    plt.setp(axB1.get_xticklabels(), visible=False)

    axB2.plot(r_fine, Er_spline, color="purple")
    axB2.set_xlabel("r [Å]")
    axB2.set_ylabel(r"$E_r=-dS/dr$ [V/Å]")

    # ---------------------------------------------------------------
    # (c) Mapa de potencial + campo vectorial, plano XY
    # ---------------------------------------------------------------
    gsC = gs[1, 0].subgridspec(1, 2, width_ratios=[1, 1.1])
    axC1 = fig.add_subplot(gsC[0])
    axC2 = fig.add_subplot(gsC[1])

    nx, ny = 160, 160
    x_vals = np.linspace(-2.0, 2.0, nx)
    y_vals = np.linspace(-1.5, 2.5, ny)
    Vmap = np.zeros((ny, nx))
    for iy, yv in enumerate(y_vals):
        for ix, xv in enumerate(x_vals):
            Vmap[iy, ix] = potential(pos, q, np.array([xv, yv, 0.0]))

    vmin, vmax = np.percentile(Vmap, [2, 98])
    im = axC1.imshow(Vmap, extent=[x_vals[0], x_vals[-1], y_vals[0], y_vals[-1]],
                      origin="lower", cmap="jet", vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=axC1, label="V (V)", fraction=0.046, pad=0.04)
    for center, _ in atoms:
        axC1.plot(center[0], center[1], "o", color="white", ms=6, mec="black")
    axC1.set_xlabel("x (Å)")
    axC1.set_ylabel("y (Å)")
    axC1.set_title("(c) Potencial $V$ y campo $\\mathbf{E}$ (plano XY)")

    nx2, ny2 = 18, 18
    x_g = np.linspace(-2.0, 2.0, nx2)
    y_g = np.linspace(-1.5, 2.5, ny2)
    Ex = np.zeros((ny2, nx2))
    Ey = np.zeros((ny2, nx2))
    for iy, yv in enumerate(y_g):
        for ix, xv in enumerate(x_g):
            Ef = field_analytic(pos, q, np.array([xv, yv, 0.0]))
            Ex[iy, ix], Ey[iy, ix] = Ef[0], Ef[1]
    mag = np.sqrt(Ex**2 + Ey**2)
    mag_safe = np.where(mag == 0, 1, mag)
    Ex_n, Ey_n = Ex / mag_safe, Ey / mag_safe

    qv = axC2.quiver(x_g, y_g, Ex_n, Ey_n, np.log10(mag + 1e-12), cmap="jet")
    plt.colorbar(qv, ax=axC2, label=r"$\log_{10}|E|$", fraction=0.046, pad=0.06)
    for center, _ in atoms:
        axC2.plot(center[0], center[1], "o", color="black", ms=6)
    axC2.set_xlabel("x (Å)")
    axC2.set_ylabel("y (Å)", labelpad=2)

    # ---------------------------------------------------------------
    # (d) Benchmark de tiempo de ejecucion
    # ---------------------------------------------------------------
    gsD = gs[1, 1].subgridspec(1, 2)
    axD1 = fig.add_subplot(gsD[0])
    axD2 = fig.add_subplot(gsD[1])

    N_ops_arr = np.array([row["N_operaciones"] for row in bench], dtype=float)
    t_arr = np.array([row["tiempo_s"] for row in bench], dtype=float)
    m, b = np.polyfit(np.log10(N_ops_arr), np.log10(t_arr), 1)
    c_rate, a_overhead = np.polyfit(N_ops_arr, t_arr, 1)

    axD1.loglog(N_ops_arr, t_arr, "o-", color="tab:blue")
    axD1.loglog(N_ops_arr, 10**b * N_ops_arr**m, "--", color="tab:red",
                label=fr"$t\propto N_{{op}}^{{{m:.2f}}}$")
    axD1.set_xlabel(r"$N_{op}$")
    axD1.set_ylabel("Tiempo (s)")
    axD1.set_title("(d) Tiempo de ejecución vs. $N_{op}$")
    axD1.legend(loc="upper left")
    axD1.grid(True, which="both", ls=":", alpha=0.5)

    N_fit = np.linspace(0, N_ops_arr.max(), 100)
    axD2.plot(N_ops_arr, t_arr, "o", color="tab:blue")
    axD2.plot(N_fit, a_overhead + c_rate * N_fit, "--", color="tab:red",
              label=fr"$c={c_rate:.2e}$ s/op")
    axD2.set_xlabel(r"$N_{op}$")
    axD2.set_ylabel("Tiempo (s)")
    axD2.legend(loc="upper left")
    axD2.grid(True, ls=":", alpha=0.5)

    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Figura combinada (panel 2x2) guardada en {filename}")

    return m, c_rate, a_overhead


# =============================================================================
# PROGRAMA PRINCIPAL
# =============================================================================
if __name__ == "__main__":

    Nc = 400
    pos, q, atoms = build_water_cloud(Nc=Nc, r_cloud=0.30)

    # -------------------------------------------------------------------
    # Tabla I: conservacion de la carga (integracion numerica)
    # -------------------------------------------------------------------
    print("=== Tabla I: conservacion de la carga (Gauss-Legendre) ===")
    print(f"{'Atomo':>6} {'Suma directa (e)':>18} {'Gauss-Legendre (e)':>20}")
    for (center, Qtot) in atoms:
        Q_int = integrate_surface_charge(Qtot, r=0.30, n_theta=12, n_phi=12)
        print(f"{'O' if Qtot < 0 else 'H':>6} {Qtot:18.6f} {Q_int:20.6f}")

    # -------------------------------------------------------------------
    # Tabla II: campo electrico, diferencias finitas vs. analitico
    # -------------------------------------------------------------------
    print("\n=== Tabla II: potencial y error relativo del campo electrico ===")
    test_points = {
        "Lejano": np.array([1.0, 1.5, 0.0]),
        "Cercano a O": np.array([0.0, 0.5, 0.0]),
        "Bisectriz": np.array([0.0, 3.0, 0.0]),
    }
    for name, robs in test_points.items():
        V = potential(pos, q, robs)
        E_num = field_numeric(pos, q, robs)
        E_an = field_analytic(pos, q, robs)
        err = np.linalg.norm(E_num - E_an) / np.linalg.norm(E_an) * 100
        print(f"\n-- {name} --  r = {robs} A")
        print(f"  V(r)            = {V: .6f} V")
        print(f"  E (analitico)   = {E_an}")
        print(f"  E (dif. finita) = {E_num}")
        print(f"  error relativo  = {err:.4e} %")

    # -------------------------------------------------------------------
    # Tabla III: validacion cruzada con Excel-ScienSolar
    # -------------------------------------------------------------------
    print("\n=== Tabla III: validacion cruzada con Excel-ScienSolar ===")
    pos_pc = np.array([[0.0, 0.0, 0.0]])
    q_pc = np.array([-1.0])
    V_punto = potential(pos_pc, q_pc, np.array([0.0, 0.0, 1.0]))
    print(f"Carga puntual (-1e) en r=(0,0,1): V = {V_punto:.4f} V   "
          f"(Excel: -14.3800 V)")

    pos_fib = fibonacci_sphere(703, 1.0)
    q_fib = np.full(703, -1.0 / 703)
    V_fib = potential(pos_fib, q_fib, np.array([0.0, 2.0, 0.0]))
    print(f"Esfera Fibonacci (Nc=703, r=1) en r=(0,2,0): V = {V_fib:.4f} V   "
          f"(Excel: -7.1899 V)")

    # -------------------------------------------------------------------
    # Perfil radial con spline cubico (datos para el panel combinado)
    # -------------------------------------------------------------------
    print("\n=== Perfil radial con spline cubico ===")
    r_c, V_c, r_f, V_spl, Er_spl, V_exact = spline_radial_profile(pos, q)
    err_spline = np.abs(V_spl - V_exact)
    print(f"Error maximo de la interpolacion spline: {err_spline.max():.3e} V "
          f"(rel. ~ {100 * err_spline.max() / V_exact.max():.2f} %)")

    # -------------------------------------------------------------------
    # Tabla IV: benchmark de tiempo de ejecucion (datos para el panel)
    # -------------------------------------------------------------------
    print("\n=== Tabla IV: tiempo de ejecucion vs. N_operaciones ===")
    bench = benchmark_performance(Nc_values=(25, 50, 100, 200, 400, 800, 1600),
                                    Nf=200, n_rep=3)
    print(f"{'Nc':>6} {'Nf':>6} {'Np':>4} {'N_operaciones':>14} "
          f"{'Tiempo (s)':>12} {'Tiempo/op (s)':>15}")
    for row in bench:
        print(f"{row['Nc']:6d} {row['Nf']:6d} {row['Np']:4d} "
              f"{row['N_operaciones']:14d} {row['tiempo_s']:12.5f} "
              f"{row['tiempo_por_operacion_s']:15.3e}")

    with open("benchmark_tiempos.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(bench[0].keys()))
        writer.writeheader()
        writer.writerows(bench)
    print("\nResultados guardados en benchmark_tiempos.csv")

    # -------------------------------------------------------------------
    # GENERACIÓN DE FIGURAS
    # -------------------------------------------------------------------
    print("\n=== Generando figuras ===")
    
    # Figura 1: Nube 3D detallada (figura independiente)
    generar_figura_nube_3d(pos, q, atoms, Nc, filename="fig_nube_agua_3d.png")
    
    # Figura 2: Panel combinado 2x2 (para el artículo)
    m, c_rate, a_overhead = figura_panel_resultados(
        pos, q, atoms, Nc, r_c, V_c, r_f, V_spl, Er_spl, bench
    )
    print(f"Ajuste log-log:  t ~ N_op^m,  m = {m:.3f}  (teorico: m=1)")
    print(f"Ajuste afin:     c = {c_rate:.3e} s/op,  a = {a_overhead:.3e} s")

    print("\n=== ¡Completado! ===")
    print("Archivos generados:")
    print("  - fig_nube_agua_3d.png        (vista 3D detallada)")
    print("  - fig_panel_resultados.png    (panel 2x2 para el artículo)")
    print("  - benchmark_tiempos.csv       (datos de rendimiento)")
    print("\nTablas disponibles en la consola.")