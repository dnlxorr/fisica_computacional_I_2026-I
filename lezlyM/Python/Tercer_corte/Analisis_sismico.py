

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

# ─── Parámetros globales de la figura ────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'serif',
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 11,
    'legend.fontsize': 9,
    'figure.dpi': 100
})

# ─────────────────────────────────────────────────────────────────────────────
# 1. MODELO DE SEÑAL SINTÉTICA
#    u(t) = sum_i A_i * exp(-xi_i * t) * sin(2*pi*f_i*t + phi_i)
# ─────────────────────────────────────────────────────────────────────────────

# Parámetros de los modos sísmicos (físicamente realistas: 0.5 – 8 Hz)
modos = [
    # (Amplitud [m], amortiguamiento [1/s], frecuencia [Hz], fase [rad])
    (1.20e-3,  0.80,  1.0,  0.00),   # modo dominante
    (0.60e-3,  1.20,  2.5,  0.30),   # segundo modo
    (0.30e-3,  2.00,  5.0,  0.60),   # tercer modo
    (0.15e-3,  3.00,  8.0,  0.90),   # componente de alta frecuencia
]


def desplazamiento(t):
    """Señal analítica de desplazamiento u(t) [m]"""
    u = np.zeros_like(t)
    for A, xi, f, phi in modos:
        u += A * np.exp(-xi * t) * np.sin(2 * np.pi * f * t + phi)
    return u


def velocidad_analitica(t):
    """Primera derivada analítica du/dt [m/s]"""
    v = np.zeros_like(t)
    for A, xi, f, phi in modos:
        omega = 2 * np.pi * f
        v += A * np.exp(-xi * t) * (
            -xi * np.sin(omega * t + phi) + omega * np.cos(omega * t + phi)
        )
    return v


def aceleracion_analitica(t):
    """Segunda derivada analítica d²u/dt² [m/s²]"""
    a = np.zeros_like(t)
    for A, xi, f, phi in modos:
        omega = 2 * np.pi * f
        a += A * np.exp(-xi * t) * (
            (xi**2 - omega**2) * np.sin(omega * t + phi)
            - 2 * xi * omega * np.cos(omega * t + phi)
        )
    return a


# ─────────────────────────────────────────────────────────────────────────────
# 2. MUESTREO Y SPLINE CÚBICO
# ─────────────────────────────────────────────────────────────────────────────

T_total = 20.0          # duración total [s]
fs_original = 100.0     # frecuencia de muestreo original [Hz]  (Δt = 0.01 s)
fs_spline   = 200.0     # frecuencia de remuestreo con spline [Hz] (Δt = 0.005 s)
# Nota: se subió fs_original de 50 a 100 Hz. A 50 Hz el error residual del
# spline (amplificado por la doble derivada) dominaba sobre el error de
# truncamiento de las diferencias finitas, haciendo que O(h⁴) saliera peor
# que O(h²) en aceleración (ver Tabla II). A 100 Hz el error de truncamiento
# vuelve a ser la fuente dominante y se recupera el orden esperado.

t_orig = np.arange(0, T_total, 1.0 / fs_original)
u_orig = desplazamiento(t_orig)

# Construcción del spline cúbico (condiciones de frontera not-a-knot)
cs = CubicSpline(t_orig, u_orig, bc_type='not-a-knot')

# Remuestreo fino
t_fine = np.arange(0, T_total, 1.0 / fs_spline)
u_fine = cs(t_fine)

print(f"Muestras originales : {len(t_orig)}")
print(f"Muestras tras spline: {len(t_fine)}")

# ─────────────────────────────────────────────────────────────────────────────
# 3. DIFERENCIAS FINITAS CENTRADAS
# ─────────────────────────────────────────────────────────────────────────────

h = t_fine[1] - t_fine[0]   # paso temporal tras remuestreo
N = len(t_fine)

# ---------- 3a. Velocidad: primera derivada ----------
v_h2 = np.zeros(N)
v_h4 = np.zeros(N)

for i in range(1, N - 1):
    v_h2[i] = (u_fine[i+1] - u_fine[i-1]) / (2*h)

for i in range(2, N - 2):
    v_h4[i] = (-u_fine[i+2] + 8*u_fine[i+1] - 8*u_fine[i-1] + u_fine[i-2]) / (12*h)

# Rellenar bordes con O(h²) para ambos
v_h2[0]  = (-3*u_fine[0] + 4*u_fine[1]  - u_fine[2])  / (2*h)
v_h2[-1] = ( 3*u_fine[-1] - 4*u_fine[-2] + u_fine[-3]) / (2*h)
v_h4[0] = v_h2[0]; v_h4[1] = v_h2[1]
v_h4[-1] = v_h2[-1]; v_h4[-2] = v_h2[-2]

# ---------- 3b. Aceleración: segunda derivada ----------
a_h2 = np.zeros(N)
a_h4 = np.zeros(N)

for i in range(1, N - 1):
    a_h2[i] = (u_fine[i+1] - 2*u_fine[i] + u_fine[i-1]) / h**2

for i in range(2, N - 2):
    a_h4[i] = (-u_fine[i+2] + 16*u_fine[i+1] - 30*u_fine[i] + 16*u_fine[i-1] - u_fine[i-2]) / (12*h**2)

a_h2[0]  = a_h2[1];  a_h2[-1]  = a_h2[-2]
a_h4[0] = a_h2[0]; a_h4[1] = a_h2[1]
a_h4[-1] = a_h2[-1]; a_h4[-2] = a_h2[-2]

# ─────────────────────────────────────────────────────────────────────────────
# 4. SOLUCIONES ANALÍTICAS DE REFERENCIA
# ─────────────────────────────────────────────────────────────────────────────

v_exact = velocidad_analitica(t_fine)
a_exact = aceleracion_analitica(t_fine)

# ─────────────────────────────────────────────────────────────────────────────
# 5. ANÁLISIS DE ERROR vs. PASO h
# ─────────────────────────────────────────────────────────────────────────────

pasos = np.logspace(-3, -0.5, 30)      # h de 0.001 s a 0.316 s
t_eval = np.linspace(1.0, 19.0, 1000)  # zona interior (evita bordes)
u_eval = desplazamiento(t_eval)
v_ref  = velocidad_analitica(t_eval)
a_ref  = aceleracion_analitica(t_eval)

err_v_h2, err_v_h4 = [], []
err_a_h2, err_a_h4 = [], []

for hh in pasos:
    v2 = (desplazamiento(t_eval + hh) - desplazamiento(t_eval - hh)) / (2*hh)
    err_v_h2.append(np.max(np.abs(v2 - v_ref)))

    v4 = (-desplazamiento(t_eval + 2*hh) + 8*desplazamiento(t_eval + hh)
          - 8*desplazamiento(t_eval - hh) + desplazamiento(t_eval - 2*hh)) / (12*hh)
    err_v_h4.append(np.max(np.abs(v4 - v_ref)))

    a2 = (desplazamiento(t_eval + hh) - 2*desplazamiento(t_eval) + desplazamiento(t_eval - hh)) / hh**2
    err_a_h2.append(np.max(np.abs(a2 - a_ref)))

    a4 = (-desplazamiento(t_eval + 2*hh) + 16*desplazamiento(t_eval + hh)
          - 30*desplazamiento(t_eval) + 16*desplazamiento(t_eval - hh)
          - desplazamiento(t_eval - 2*hh)) / (12*hh**2)
    err_a_h4.append(np.max(np.abs(a4 - a_ref)))

err_v_h2 = np.array(err_v_h2)
err_v_h4 = np.array(err_v_h4)
err_a_h2 = np.array(err_a_h2)
err_a_h4 = np.array(err_a_h4)

# ─────────────────────────────────────────────────────────────────────────────
# 6. MÉTRICAS SÍSMICAS
# ─────────────────────────────────────────────────────────────────────────────

PGD = np.max(np.abs(u_fine))                # Peak Ground Displacement [m]
PGV = np.max(np.abs(v_h4))                  # Peak Ground Velocity [m/s]
PGA = np.max(np.abs(a_h4))                  # Peak Ground Acceleration [m/s²]
PGA_g = PGA / 9.81                          # PGA en fracción de g

print(f"\n── Métricas sísmicas (spline + DF O(h⁴)) ──")
print(f"PGD = {PGD*100:.4f} cm")
print(f"PGV = {PGV*100:.4f} cm/s")
print(f"PGA = {PGA:.4f} m/s²  ({PGA_g:.4f} g)")

# Error máximo en zona interior
idx = slice(10, -10)
err_v_max_h2 = np.max(np.abs(v_h2[idx] - v_exact[idx]))
err_v_max_h4 = np.max(np.abs(v_h4[idx] - v_exact[idx]))
err_a_max_h2 = np.max(np.abs(a_h2[idx] - a_exact[idx]))
err_a_max_h4 = np.max(np.abs(a_h4[idx] - a_exact[idx]))

print(f"\n── Error máximo (h = {h:.4f} s) ──")
print(f"Velocidad  O(h²): {err_v_max_h2:.3e} m/s")
print(f"Velocidad  O(h⁴): {err_v_max_h4:.3e} m/s")
print(f"Aceleración O(h²): {err_a_max_h2:.3e} m/s²")
print(f"Aceleración O(h⁴): {err_a_max_h4:.3e} m/s²")

# ─────────────────────────────────────────────────────────────────────────────
# 7. FIGURAS  (se MUESTRAN en pantalla, no se guardan en disco)
# ─────────────────────────────────────────────────────────────────────────────

COLORS = {
    'exact': '#2C2C2A',
    'h2':    '#185FA5',
    'h4':    '#0F6E56',
    'orig':  '#BA7517',
    'error': '#993C1D',
}

# ── Figura 1: Señal original, spline, y derivadas ────────────────────────────
fig1, axes = plt.subplots(3, 1, figsize=(9, 8), sharex=True)
fig1.suptitle("Señal sísmica sintética: desplazamiento, velocidad y aceleración",
              fontsize=12, y=0.98)

ax = axes[0]
ax.plot(t_fine, u_fine * 1e3, color=COLORS['exact'], lw=1.2, label='Spline cúbico')
ax.plot(t_orig, u_orig * 1e3, 'o', color=COLORS['orig'], ms=2.5, alpha=0.6, label='Muestras originales')
ax.set_ylabel('Desplazamiento (mm)')
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, lw=0.5)

ax = axes[1]
ax.plot(t_fine, v_exact * 1e2,  color=COLORS['exact'], lw=1.5, label='Analítica')
ax.plot(t_fine, v_h2    * 1e2,  color=COLORS['h2'],    lw=1.0, ls='--', label='DF O(h²)')
ax.plot(t_fine, v_h4    * 1e2,  color=COLORS['h4'],    lw=1.0, ls=':',  label='DF O(h⁴)')
ax.set_ylabel('Velocidad (cm/s)')
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, lw=0.5)

ax = axes[2]
ax.plot(t_fine, a_exact, color=COLORS['exact'], lw=1.5, label='Analítica')
ax.plot(t_fine, a_h2,    color=COLORS['h2'],    lw=1.0, ls='--', label='DF O(h²)')
ax.plot(t_fine, a_h4,    color=COLORS['h4'],    lw=1.0, ls=':',  label='DF O(h⁴)')
ax.axhline(PGA,  ls='--', color='#E24B4A', lw=0.8, alpha=0.7)
ax.axhline(-PGA, ls='--', color='#E24B4A', lw=0.8, alpha=0.7, label=f'PGA = {PGA:.3f} m/s²')
ax.set_ylabel('Aceleración (m/s²)')
ax.set_xlabel('Tiempo (s)')
ax.legend(loc='upper right', framealpha=0.9)
ax.grid(True, alpha=0.3, lw=0.5)

plt.tight_layout()

# ── Figura 2: Error puntual en zona central ───────────────────────────────────
t_zone = t_fine[idx]

fig2, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
fig2.suptitle("Error puntual de diferencias finitas respecto a la solución analítica", fontsize=12)

axes[0].semilogy(t_zone, np.abs(v_h2[idx] - v_exact[idx]), color=COLORS['h2'], lw=1.0, label='O(h²)')
axes[0].semilogy(t_zone, np.abs(v_h4[idx] - v_exact[idx]), color=COLORS['h4'], lw=1.0, ls='--', label='O(h⁴)')
axes[0].set_ylabel('|Error| velocidad (m/s)')
axes[0].legend(); axes[0].grid(True, alpha=0.3, lw=0.5)

axes[1].semilogy(t_zone, np.abs(a_h2[idx] - a_exact[idx]), color=COLORS['h2'], lw=1.0, label='O(h²)')
axes[1].semilogy(t_zone, np.abs(a_h4[idx] - a_exact[idx]), color=COLORS['h4'], lw=1.0, ls='--', label='O(h⁴)')
axes[1].set_ylabel('|Error| aceleración (m/s²)')
axes[1].set_xlabel('Tiempo (s)')
axes[1].legend(); axes[1].grid(True, alpha=0.3, lw=0.5)

plt.tight_layout()

# ── Figura 3: Análisis log-log error vs h ─────────────────────────────────────
fig3, axes = plt.subplots(1, 2, figsize=(10, 4.5))
fig3.suptitle("Convergencia del error de truncamiento vs. paso h", fontsize=12)

for ax, err2, err4, titulo in [
    (axes[0], err_v_h2, err_v_h4, "Primera derivada (velocidad)"),
    (axes[1], err_a_h2, err_a_h4, "Segunda derivada (aceleración)"),
]:
    ax.loglog(pasos, err2, 'o-', color=COLORS['h2'], ms=4, lw=1.2, label='O(h²)')
    ax.loglog(pasos, err4, 's-', color=COLORS['h4'], ms=4, lw=1.2, label='O(h⁴)')

    idx_ref = 10
    c2 = err2[idx_ref] / pasos[idx_ref]**2
    c4 = err4[idx_ref] / pasos[idx_ref]**4
    ax.loglog(pasos, c2 * pasos**2, '--', color=COLORS['h2'], lw=0.8, alpha=0.6, label='~ h²')
    ax.loglog(pasos, c4 * pasos**4, '--', color=COLORS['h4'], lw=0.8, alpha=0.6, label='~ h⁴')

    ax.set_xlabel('Paso temporal h (s)')
    ax.set_ylabel('Error máximo')
    ax.set_title(titulo)
    ax.legend(fontsize=8)
    ax.grid(True, which='both', alpha=0.3, lw=0.5)

plt.tight_layout()

# ── Figura 4: Spline — comparación con muestras gruesas ──────────────────────
t_grueso = np.arange(0, T_total, 0.5)   # 2 Hz (muy escaso)
u_grueso = desplazamiento(t_grueso)
cs_grueso = CubicSpline(t_grueso, u_grueso, bc_type='not-a-knot')
u_spline_grueso = cs_grueso(t_fine)
u_spline_fino   = cs(t_fine)
u_ref_fino      = desplazamiento(t_fine)

fig4, axes = plt.subplots(2, 1, figsize=(9, 5.5))
fig4.suptitle("Efecto del spline cúbico en la reconstrucción de la señal", fontsize=12)

axes[0].plot(t_fine, u_ref_fino  * 1e3, color=COLORS['exact'], lw=1.5, label='Señal exacta')
axes[0].plot(t_fine, u_spline_fino * 1e3, color=COLORS['h4'], lw=1.0, ls='--', label=f'Spline (fs = {int(fs_original)} Hz)')
axes[0].plot(t_grueso, u_grueso * 1e3, 'o', color=COLORS['orig'], ms=4, label='Muestras (fs = 2 Hz)')
axes[0].plot(t_fine, u_spline_grueso * 1e3, color=COLORS['error'], lw=1.0, ls=':', label='Spline (fs = 2 Hz)')
axes[0].set_ylabel('Desplazamiento (mm)')
axes[0].set_xlim(0, 6)
axes[0].legend(fontsize=8)
axes[0].grid(True, alpha=0.3, lw=0.5)

axes[1].semilogy(t_fine, np.abs(u_spline_fino - u_ref_fino) * 1e3,
                  color=COLORS['h4'], lw=1.0, label=f'Error spline {int(fs_original)} Hz')
axes[1].semilogy(t_fine, np.abs(u_spline_grueso - u_ref_fino) * 1e3,
                  color=COLORS['error'], lw=1.0, label='Error spline 2 Hz')
axes[1].set_ylabel('|Error spline| (mm)')
axes[1].set_xlabel('Tiempo (s)')
axes[1].set_xlim(0, 6)
axes[1].legend(fontsize=8)
axes[1].grid(True, which='both', alpha=0.3, lw=0.5)

plt.tight_layout()

print("\n✓ Todas las figuras generadas correctamente (se muestran en pantalla).")
print(f"\n── Tabla resumen de errores (h = {h:.4f} s) ──")
print(f"{'Cantidad':<25} {'O(h²)':<20} {'O(h⁴)':<20} {'Mejora'}")
print("-"*75)
print(f"{'Vel. max |error|':<25} {err_v_max_h2:.3e} m/s       {err_v_max_h4:.3e} m/s       {err_v_max_h2/err_v_max_h4:.1f}×")
print(f"{'Acel. max |error|':<25} {err_a_max_h2:.3e} m/s²      {err_a_max_h4:.3e} m/s²      {err_a_max_h2/err_a_max_h4:.1f}×")

# Mostrar todas las figuras al final (bloquea hasta que se cierren las ventanas)
plt.show()