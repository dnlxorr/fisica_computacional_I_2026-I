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
        - fig_nube_agua_xy.png        (Fig. 1 del articulo)
        - spline_potencial.png        (Fig. 2 del articulo)
        - fig_potencial_campo_combo.png (Fig. 3 del articulo)
        - fig_benchmark_tiempos.png   (Fig. 4 del articulo)

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


# =============================================================================
# 0. CONSTANTES FISICAS
# =============================================================================
k_SI = 8.9875517923e9      # Constante de Coulomb, N m^2 / C^2
e_C = 1.602176634e-19      # Carga elemental, C
ANG = 1.0e-10               # 1 Angstrom en metros

# Constante efectiva para trabajar directamente en unidades (Angstrom, e, V):
#   V [V] = K_EFF * q [e] / r [Angstrom]
# Este valor (~14.38) es exactamente el reportado en la Tabla 2 del articulo
# de Excel para una carga puntual de -1e a 1 Angstrom (V = -14.38 V), lo que
# permite usar esa tabla como prueba unitaria del codigo (ver Seccion 5).
K_EFF = k_SI * e_C / ANG


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
    filas, de modo que el unico parametro que cambia sea N_operaciones.
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
# FIGURAS (una funcion por figura del articulo)
# =============================================================================
def fig1_nube_xy(pos, q, atoms, Nc, filename="fig_nube_agua_xy.png"):
    """
    Figura 1 del articulo: proyeccion en el plano xy de las tres nubes de
    Fibonacci. Confirma visualmente que r_cloud=0.30 A es consistente con
    r_OH=0.9572 A (las nubes no se superponen).
    """
    colors = ["tab:red", "tab:blue", "tab:blue"]
    labels = ["O", "H1", "H2"]

    fig, ax = plt.subplots(figsize=(5, 5))
    for i, (center, _) in enumerate(atoms):
        sl = slice(i * Nc, (i + 1) * Nc)
        ax.scatter(pos[sl, 0], pos[sl, 1], s=4, color=colors[i], label=labels[i])
        ax.plot(center[0], center[1], "o", color="black", ms=5)
    ax.set_xlabel("x (Å)")
    ax.set_ylabel("y (Å)")
    ax.set_title(r"Nube de cargas H$_2$O - Vista 2D (Plano XY)")
    ax.legend()
    ax.set_aspect("equal")
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Figura guardada en {filename}")


def fig2_spline(r_coarse, V_coarse, r_fine, V_fine_spline, Er_spline,
                 filename="spline_potencial.png"):
    """
    Figura 2 del articulo: potencial V(r) sobre la bisectriz H-O-H
    (evaluacion exacta vs. spline cubico de 8 nodos) y campo radial
    E_r = -dS/dr obtenido por derivacion del spline.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(5, 6), sharex=True)

    ax1.plot(r_fine, V_fine_spline, "--", color="black", label="Spline cubico", zorder=2)
    ax1.plot(r_fine, V_fine_spline, color="tab:blue", lw=2, alpha=0.0)  # placeholder
    ax1.plot(r_coarse, V_coarse, "o", color="red", ms=8, label="Nodos del spline (8 pts)", zorder=3)
    ax1.set_ylabel("V(r) [V]")
    ax1.set_title("Potencial sobre la bisectriz H-O-H")
    ax1.legend(fontsize=8)

    ax2.plot(r_fine, Er_spline, color="purple")
    ax2.set_xlabel("r [Angstrom]")
    ax2.set_ylabel(r"$E_r = -dS/dr$ [V/A]")

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Figura guardada en {filename}")


def fig3_potencial_y_campo(pos, q, atoms, filename="fig_potencial_campo_combo.png"):
    """
    Figura 3 del articulo: mapa de potencial V(x,y) (panel izquierdo) y
    campo electrico E(x,y) (panel derecho), en el plano molecular.

    Decisiones de visualizacion (no afectan ningun calculo, solo la forma
    de mostrarlo):
      - El rango de color de V se recorta al percentil 2-98, porque cada
        subelemento sigue siendo una carga puntual y V diverge cerca de
        cada nucleo; sin el recorte, esas pocas singularidades "aplastan"
        la escala de color y se pierde la forma del potencial molecular.
      - Las flechas de E se normalizan a longitud unitaria (se grafica la
        DIRECCION), porque |E| varia varios ordenes de magnitud entre el
        entorno nuclear y el campo lejano; la magnitud perdida se recupera
        coloreando las flechas con log10|E|.
    """
    # ---- Malla fina para el mapa de potencial ----
    nx, ny = 220, 220
    x_vals = np.linspace(-2.0, 2.0, nx)
    y_vals = np.linspace(-1.5, 2.5, ny)
    Vmap = np.zeros((ny, nx))
    for iy, yv in enumerate(y_vals):
        for ix, xv in enumerate(x_vals):
            Vmap[iy, ix] = potential(pos, q, np.array([xv, yv, 0.0]))

    # ---- Malla gruesa para el campo vectorial ----
    nx2, ny2 = 22, 22
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

    # ---- Figura de dos paneles ----
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 4.5))

    vmin, vmax = np.percentile(Vmap, [2, 98])
    im = axL.imshow(Vmap, extent=[x_vals[0], x_vals[-1], y_vals[0], y_vals[-1]],
                     origin="lower", cmap="jet", vmin=vmin, vmax=vmax)
    plt.colorbar(im, ax=axL, label="V (V)")
    for center, _ in atoms:
        axL.plot(center[0], center[1], "o", color="white", ms=6, mec="black")
    axL.set_xlabel("x (Å)")
    axL.set_ylabel("y (Å)")
    axL.set_title(r"Mapa de potencial electrostático (Plano XY) - H$_2$O")

    qv = axR.quiver(x_g, y_g, Ex_n, Ey_n, np.log10(mag + 1e-12), cmap="jet")
    plt.colorbar(qv, ax=axR, label=r"$\log_{10}|E|$ (V/Å)")
    for center, _ in atoms:
        axR.plot(center[0], center[1], "o", color="black", ms=6)
    axR.set_xlabel("x (Å)")
    axR.set_ylabel("y (Å)")
    axR.set_title(r"Campo eléctrico (dirección en Plano XY) - H$_2$O")

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Figura guardada en {filename}")


def fig4_benchmark(bench, filename="fig_benchmark_tiempos.png"):
    """
    Figura 4 del articulo: tiempo de ejecucion vs. N_operaciones, en dos
    representaciones (log-log y lineal con ajuste afin).
    """
    N_ops_arr = np.array([row["N_operaciones"] for row in bench], dtype=float)
    t_arr = np.array([row["tiempo_s"] for row in bench], dtype=float)

    # Ajuste 1 (log-log): t ~ N_op^m
    m, b = np.polyfit(np.log10(N_ops_arr), np.log10(t_arr), 1)

    # Ajuste 2 (afin): t = a + c*N_op  (separa overhead "a" del costo
    # asintotico por operacion "c", que es el comparable con la Tabla 1
    # del articulo de Excel)
    c_rate, a_overhead = np.polyfit(N_ops_arr, t_arr, 1)

    print(f"\nAjuste log-log:  t ~ N_op^m,  m = {m:.3f}  (teorico: m=1)")
    print(f"Ajuste afin:     t = a + c*N_op")
    print(f"   c (tiempo asintotico por operacion) = {c_rate:.3e} s")
    print(f"   a (overhead total)                  = {a_overhead:.3e} s")

    fig, (axA, axB) = plt.subplots(1, 2, figsize=(10, 4.2))

    axA.loglog(N_ops_arr, t_arr, "o-", color="tab:blue", label="Medido (Python)")
    axA.loglog(N_ops_arr, 10**b * N_ops_arr**m, "--", color="tab:red",
               label=fr"$t \propto N_{{op}}^{{{m:.2f}}}$")
    axA.set_xlabel(r"$N_{operaciones}=N_f N_c N_p$")
    axA.set_ylabel("Tiempo (s)")
    axA.set_title("Escala log-log")
    axA.legend(fontsize=8)
    axA.grid(True, which="both", ls=":", alpha=0.5)

    axB.plot(N_ops_arr, t_arr, "o", color="tab:blue", label="Medido (Python)")
    N_fit = np.linspace(0, N_ops_arr.max(), 100)
    axB.plot(N_fit, a_overhead + c_rate * N_fit, "--", color="tab:red",
             label=fr"$t=a+cN_{{op}}$" + "\n" +
                   fr"$c={c_rate:.2e}$ s/op" + "\n" +
                   fr"$a={a_overhead:.2e}$ s")
    axB.set_xlabel(r"$N_{operaciones}=N_f N_c N_p$")
    axB.set_ylabel("Tiempo (s)")
    axB.set_title("Escala lineal (ajuste afín)")
    axB.legend(fontsize=8)
    axB.grid(True, ls=":", alpha=0.5)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"Figura guardada en {filename}")

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
    # Figura 1: nube 2D en el plano XY
    # -------------------------------------------------------------------
    print("\n=== Figura 1: nube de cargas (plano XY) ===")
    fig1_nube_xy(pos, q, atoms, Nc)

    # -------------------------------------------------------------------
    # Figura 2: perfil radial con spline cubico
    # -------------------------------------------------------------------
    print("\n=== Figura 2: perfil radial con spline cubico ===")
    r_c, V_c, r_f, V_spl, Er_spl, V_exact = spline_radial_profile(pos, q)
    err_spline = np.abs(V_spl - V_exact)
    print(f"Error maximo de la interpolacion spline: {err_spline.max():.3e} V "
          f"(rel. ~ {100 * err_spline.max() / V_exact.max():.2f} %)")
    fig2_spline(r_c, V_c, r_f, V_spl, Er_spl)

    # -------------------------------------------------------------------
    # Figura 3: mapa de potencial + campo vectorial (plano XY)
    # -------------------------------------------------------------------
    print("\n=== Figura 3: mapa de potencial y campo vectorial ===")
    fig3_potencial_y_campo(pos, q, atoms)

    # -------------------------------------------------------------------
    # Tabla IV y Figura 4: benchmark de tiempo de ejecucion
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

    fig4_benchmark(bench)

    print("\n=== Listo. Todas las tablas y figuras del articulo fueron generadas. ===")