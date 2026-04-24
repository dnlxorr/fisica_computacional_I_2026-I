"""
Partícula con fuerza constante y velocidad inicial arbitraria (no paralelas)
=============================================================================
F = constante → solución analítica exacta disponible → podemos medir el error real
Métodos numéricos: Trapecio y Simpson 1/3
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# ─────────────────────────────────────────────────────────────
# PARÁMETROS  (modifica estos valores libremente)
# ─────────────────────────────────────────────────────────────
m = 2.0  # masa [kg]

# Velocidad inicial — dirección arbitraria
v0x = 4.0  # [m/s]
v0y = 6.0  # [m/s]

# Fuerza constante — NO paralela a v0
# Para garantizarlo: (Fx/Fy) ≠ (v0x/v0y), es decir los vectores no proporcionales
Fx_cte = 3.0  # [N]
Fy_cte = -9.0  # [N]   (componente hacia abajo, como gravedad pero más fuerte)

# Posición inicial
x0 = 0.0
y0 = 0.0

# Tiempo
t_ini = 0.0
t_fin = 5.0
N = 100  # número de intervalos (deliberadamente bajo para ver el error)

# ─────────────────────────────────────────────────────────────
# VERIFICAR QUE F y v0 NO SON PARALELAS
# Dos vectores son paralelos si su producto cruzado es cero
# producto cruzado 2D: v0x*Fy - v0y*Fx
# ─────────────────────────────────────────────────────────────
cross = v0x * Fy_cte - v0y * Fx_cte
angulo = np.degrees(np.arccos(
    np.dot([v0x, v0y], [Fx_cte, Fy_cte]) /
    (np.linalg.norm([v0x, v0y]) * np.linalg.norm([Fx_cte, Fy_cte]))
))
print(f"Ángulo entre v₀ y F: {angulo:.2f}°")
if abs(cross) < 1e-10:
    raise ValueError("¡v₀ y F son paralelas! Cambia los valores.")
else:
    print(f"✓ Vectores NO paralelos (producto cruzado = {cross:.2f})")

# ─────────────────────────────────────────────────────────────
# ACELERACIÓN CONSTANTE
# ─────────────────────────────────────────────────────────────
acx = Fx_cte / m  # [m/s²]
acy = Fy_cte / m  # [m/s²]
print(f"Aceleración: ax={acx} m/s², ay={acy} m/s²")


# ─────────────────────────────────────────────────────────────
# SOLUCIÓN ANALÍTICA EXACTA
# v(t) = v0 + a*t
# x(t) = x0 + v0*t + (1/2)*a*t²
# ─────────────────────────────────────────────────────────────
def vx_analitico(t): return v0x + acx * t


def vy_analitico(t): return v0y + acy * t


def x_analitico(t):  return x0 + v0x * t + 0.5 * acx * t ** 2


def y_analitico(t):  return y0 + v0y * t + 0.5 * acy * t ** 2


# ─────────────────────────────────────────────────────────────
# FUNCIONES DE INTEGRACIÓN NUMÉRICA ACUMULATIVA
# ─────────────────────────────────────────────────────────────

def integrar_trapecio(f_vals, h):
    integral = np.zeros(len(f_vals))
    for i in range(1, len(f_vals)):
        integral[i] = integral[i - 1] + (h / 2.0) * (f_vals[i - 1] + f_vals[i])
    return integral


def integrar_simpson(f_vals, h):
    n = len(f_vals)
    integral = np.zeros(n)

    for i in range(2, n, 2):
        integral[i] = integral[i-2] + (h/3)*(f_vals[i-2] + 4*f_vals[i-1] + f_vals[i])

    # NO interpolar agresivamente
    for i in range(1, n, 2):
        integral[i] = integral[i-1]  # o simplemente déjalos así

    return integral


# ─────────────────────────────────────────────────────────────
# ARREGLO DE TIEMPO
# ─────────────────────────────────────────────────────────────
if N % 2 != 0:
    N += 1  # Simpson necesita N par

t = np.linspace(t_ini, t_fin, N + 1)
h = t[1] - t[0]

# Aceleración evaluada en cada punto de tiempo (constante → array uniforme)
ax_vals = np.full(len(t), acx)
ay_vals = np.full(len(t), acy)

# ─────────────────────────────────────────────────────────────
# PASO 1: Integrar aceleración → velocidad
# ─────────────────────────────────────────────────────────────
# Trapecio
vx_trap = v0x + integrar_trapecio(ax_vals, h)
vy_trap = v0y + integrar_trapecio(ay_vals, h)

# Simpson
vx_simp = v0x + integrar_simpson(ax_vals, h)
vy_simp = v0y + integrar_simpson(ay_vals, h)

# ─────────────────────────────────────────────────────────────
# PASO 2: Integrar velocidad → posición
# ─────────────────────────────────────────────────────────────
# Trapecio
x_trap = x0 + integrar_trapecio(vx_trap, h)
y_trap = y0 + integrar_trapecio(vy_trap, h)

# Simpson
x_simp = x0 + integrar_simpson(vx_simp, h)
y_simp = y0 + integrar_simpson(vy_simp, h)

# ─────────────────────────────────────────────────────────────
# SOLUCIÓN ANALÍTICA SOBRE EL MISMO ARREGLO t
# ─────────────────────────────────────────────────────────────
x_exact = x_analitico(t)
y_exact = y_analitico(t)
vx_exact = vx_analitico(t)
vy_exact = vy_analitico(t)

# ─────────────────────────────────────────────────────────────
# ERRORES ABSOLUTOS respecto a la solución exacta
# ─────────────────────────────────────────────────────────────
err_x_trap = np.abs(x_trap - x_exact)
err_y_trap = np.abs(y_trap - y_exact)
err_x_simp = np.abs(x_simp - x_exact)
err_y_simp = np.abs(y_simp - y_exact)

print(f"\nError máximo en x  →  Trapecio: {err_x_trap.max():.4e} m  |  Simpson: {err_x_simp.max():.4e} m")
print(f"Error máximo en y  →  Trapecio: {err_y_trap.max():.4e} m  |  Simpson: {err_y_simp.max():.4e} m")

# ─────────────────────────────────────────────────────────────
# GRAFICACIÓN
# ─────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor':   '#10102a',
    'text.color':       'white',
    'axes.labelcolor':  '#aaaacc',
    'xtick.color':      'white',
    'ytick.color':      'white',
    'axes.edgecolor':   '#333355',
    'grid.color':       '#333355',
})
fig = plt.figure(figsize=(18, 14), facecolor='#0a0a1a')
gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.50, wspace=0.38)

C_TRAP = '#00d4ff'  # azul cyan  → Trapecio
C_SIMP = '#ff6b6b'  # rojo coral → Simpson
C_EXACT = '#aaffaa'  # verde suave → Exacta
C_FX = '#ffd166'  # amarillo   → Fx
C_FY = '#06d6a0'  # verde      → Fy

kw_ax = dict(color='white', fontsize=11, fontweight='bold', pad=8)
kw_label = dict(color='#aaaacc', fontsize=9)
kw_bg = dict(facecolor='#10102a')

# ── 1. Vectores F y v0 (ilustración) ────────────────────────
a1 = fig.add_subplot(gs[0, 0])
a1.set_facecolor('#10102a')
a1.quiver(0, 0, v0x, v0y, angles='xy', scale_units='xy', scale=1,
          color=C_EXACT, width=0.015, label=f'v₀ = ({v0x},{v0y}) m/s')
a1.quiver(0, 0, Fx_cte, Fy_cte, angles='xy', scale_units='xy', scale=1,
          color=C_FX, width=0.015, label=f'F = ({Fx_cte},{Fy_cte}) N')
lim = max(abs(v0x), abs(v0y), abs(Fx_cte), abs(Fy_cte)) * 1.3
a1.set_xlim(-lim, lim);
a1.set_ylim(-lim, lim)
a1.axhline(0, color='gray', lw=0.5);
a1.axvline(0, color='gray', lw=0.5)
a1.set_title(f'Vectores iniciales\nÁngulo = {angulo:.1f}°', **kw_ax)
a1.set_xlabel('x', **kw_label);
a1.set_ylabel('y', **kw_label)
a1.legend(fontsize=9, framealpha=0.2)
a1.grid(alpha=0.15)
a1.set_aspect('equal')

# ── 2. Velocidad Vx(t) ──────────────────────────────────────
a2 = fig.add_subplot(gs[0, 1])
a2.plot(t, vx_exact, color=C_EXACT, lw=2.5, label='Exacta', zorder=3)
a2.plot(t, vx_trap, color=C_TRAP, lw=1.5, ls='--', label='Trapecio')
a2.plot(t, vx_simp, color=C_SIMP, lw=1.5, ls=':', label='Simpson')
a2.set_title('Velocidad Vx(t)', **kw_ax)
a2.set_xlabel('t [s]', **kw_label);
a2.set_ylabel('Vx [m/s]', **kw_label)
a2.legend(fontsize=9, framealpha=0.2);
a2.grid(alpha=0.15);
a2.set_facecolor('#10102a')

# ── 3. Velocidad Vy(t) ──────────────────────────────────────
a3 = fig.add_subplot(gs[0, 2])
a3.plot(t, vy_exact, color=C_EXACT, lw=2.5, label='Exacta', zorder=3)
a3.plot(t, vy_trap, color=C_TRAP, lw=1.5, ls='--', label='Trapecio')
a3.plot(t, vy_simp, color=C_SIMP, lw=1.5, ls=':', label='Simpson')
a3.set_title('Velocidad Vy(t)', **kw_ax)
a3.set_xlabel('t [s]', **kw_label);
a3.set_ylabel('Vy [m/s]', **kw_label)
a3.legend(fontsize=9, framealpha=0.2);
a3.grid(alpha=0.15);
a3.set_facecolor('#10102a')

# ── 4. Posición X(t) ────────────────────────────────────────
a4 = fig.add_subplot(gs[1, 0])
a4.plot(t, x_exact, color=C_EXACT, lw=2.5, label='Exacta', zorder=3)
a4.plot(t, x_trap, color=C_TRAP, lw=1.5, ls='--', label='Trapecio')
a4.plot(t, x_simp, color=C_SIMP, lw=1.5, ls=':', label='Simpson')
a4.set_title('Posición X(t)', **kw_ax)
a4.set_xlabel('t [s]', **kw_label);
a4.set_ylabel('x [m]', **kw_label)
a4.legend(fontsize=9, framealpha=0.2);
a4.grid(alpha=0.15);
a4.set_facecolor('#10102a')

# ── 5. Posición Y(t) ────────────────────────────────────────
a5 = fig.add_subplot(gs[1, 1])
a5.plot(t, y_exact, color=C_EXACT, lw=2.5, label='Exacta', zorder=3)
a5.plot(t, y_trap, color=C_TRAP, lw=1.5, ls='--', label='Trapecio')
a5.plot(t, y_simp, color=C_SIMP, lw=1.5, ls=':', label='Simpson')
a5.set_title('Posición Y(t)', **kw_ax)
a5.set_xlabel('t [s]', **kw_label);
a5.set_ylabel('y [m]', **kw_label)
a5.legend(fontsize=9, framealpha=0.2);
a5.grid(alpha=0.15);
a5.set_facecolor('#10102a')

# ── 6. Trayectoria 2D ───────────────────────────────────────
a6 = fig.add_subplot(gs[1, 2])
a6.plot(x_exact, y_exact, color=C_EXACT, lw=2.5, label='Exacta', zorder=3)
a6.plot(x_trap, y_trap, color=C_TRAP, lw=1.5, ls='--', label='Trapecio')
a6.plot(x_simp, y_simp, color=C_SIMP, lw=1.5, ls=':', label='Simpson')
a6.scatter([x0], [y0], color='white', s=80, zorder=5, label='Inicio')
a6.set_title('Trayectoria 2D (parábola)', **kw_ax)
a6.set_xlabel('x [m]', **kw_label);
a6.set_ylabel('y [m]', **kw_label)
a6.legend(fontsize=9, framealpha=0.2);
a6.grid(alpha=0.15);
a6.set_facecolor('#10102a')

# ── 7. Error absoluto en X ──────────────────────────────────
a7 = fig.add_subplot(gs[2, 0])
a7.semilogy(t, err_x_trap + 1e-15, color=C_TRAP, lw=2, label='Trapecio')
a7.semilogy(t, err_x_simp + 1e-15, color=C_SIMP, lw=2, ls='--', label='Simpson')
a7.set_title('Error absoluto en X\nvs solución exacta', **kw_ax)
a7.set_xlabel('t [s]', **kw_label);
a7.set_ylabel('|error| [m]', **kw_label)
a7.legend(fontsize=9, framealpha=0.2);
a7.grid(alpha=0.15, which='both');
a7.set_facecolor('#10102a')

# ── 8. Error absoluto en Y ──────────────────────────────────
a8 = fig.add_subplot(gs[2, 1])
a8.semilogy(t, err_y_trap + 1e-15, color=C_TRAP, lw=2, label='Trapecio')
a8.semilogy(t, err_y_simp + 1e-15, color=C_SIMP, lw=2, ls='--', label='Simpson')
a8.set_title('Error absoluto en Y\nvs solución exacta', **kw_ax)
a8.set_xlabel('t [s]', **kw_label);
a8.set_ylabel('|error| [m]', **kw_label)
a8.legend(fontsize=9, framealpha=0.2);
a8.grid(alpha=0.15, which='both');
a8.set_facecolor('#10102a')

# ── 9. Tabla resumen de errores ─────────────────────────────
a9 = fig.add_subplot(gs[2, 2])
a9.axis('off')
a9.set_facecolor('#10102a')
tabla_data = [
    ['', 'Trapecio', 'Simpson'],
    ['Error máx X [m]', f'{err_x_trap.max():.3e}', f'{err_x_simp.max():.3e}'],
    ['Error máx Y [m]', f'{err_y_trap.max():.3e}', f'{err_y_simp.max():.3e}'],
    ['Orden del error', 'O(h²)', 'O(h⁴)'],
    ['N pasos', str(N), str(N)],
    ['h [s]', f'{h:.4f}', f'{h:.4f}'],
]
tabla = a9.table(
    cellText=tabla_data,
    cellLoc='center', loc='center',
    bbox=[0, 0.1, 1, 0.85]
)
tabla.auto_set_font_size(False)
tabla.set_fontsize(9)
for (r, c), cell in tabla.get_celld().items():
    cell.set_facecolor('#1a1a3a' if r % 2 == 0 else '#22224a')
    cell.set_text_props(color='white')
    cell.set_edgecolor('#333355')
a9.set_title('Resumen de precisión', **kw_ax)

# ── Título global ────────────────────────────────────────────
fig.suptitle(
    f'Partícula  m={m} kg  |  v₀=({v0x}, {v0y}) m/s  |  F=({Fx_cte}, {Fy_cte}) N  |  Ángulo={angulo:.1f}°  |  N={N} pasos',
    color='white', fontsize=13, fontweight='bold', y=0.99
)

plt.savefig('particula_fuerza_cte.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()
print("\n✅ Gráfica guardada.")