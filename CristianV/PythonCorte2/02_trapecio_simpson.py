"""
INTEGRACIÓN NUMÉRICA I: Regla del Trapecio, Simpson y comparación de errores
Función de prueba: f(x) = x² · e^(-x)  en [0, 5]
Valor exacto: ∫₀⁵ x²·e^(-x) dx = 2 - 27·e^(-5)  ≈ 1.8352
Esta función tiene forma de campana asimétrica → no trivial
"""

import numpy as np
import matplotlib.pyplot as plt

# ─────────────────────────────────────────────────────────────
# Función y valor exacto
# ─────────────────────────────────────────────────────────────
def f(x):
    return x**2 * np.exp(-x)

a, b = 0, 5
# Valor exacto obtenido por integración por partes:
# ∫ x²e^(-x)dx = -e^(-x)(x² + 2x + 2) → evaluado en [0,5]
I_exacto = (-np.exp(-b)*(b**2 + 2*b + 2)) - (-np.exp(-a)*(a**2 + 2*a + 2))

# ─────────────────────────────────────────────────────────────
# REGLA DEL TRAPECIO
# Divide [a,b] en n subintervalos iguales de ancho h.
# En cada uno aproxima el área como un trapecio:
#   Área_i = h/2 · (f(xᵢ) + f(xᵢ₊₁))
# Fórmula compuesta: h/2·[f(x₀) + 2f(x₁) + ... + 2f(xₙ₋₁) + f(xₙ)]
# Error global ~ O(h²): si duplicamos n, el error cae 4 veces
# ─────────────────────────────────────────────────────────────
def trapecio(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2)

# ─────────────────────────────────────────────────────────────
# REGLA DE SIMPSON 1/3
# En cada par de subintervalos ajusta una parábola (no una recta).
# Fórmula: h/3·[f(x₀) + 4f(x₁) + 2f(x₂) + 4f(x₃) + ... + f(xₙ)]
# El patrón 1-4-2-4-2-...-4-1 viene de integrar la parábola exacta.
# Error global ~ O(h⁴): si duplicamos n, el error cae 16 veces.
# REQUIERE n par.
# ─────────────────────────────────────────────────────────────
def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])

# ─────────────────────────────────────────────────────────────
# Calcular errores para distintos n
# ─────────────────────────────────────────────────────────────
N_vals = np.arange(2, 60, 2)
err_trap = [abs(trapecio(f, a, b, n) - I_exacto) for n in N_vals]
err_simp = [abs(simpson( f, a, b, n) - I_exacto) for n in N_vals]

# ─────────────────────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Integración Numérica I — f(x) = x²·e⁻ˣ,  I_exacto = {:.6f}".format(I_exacto),
             fontsize=13, fontweight='bold')

# Panel 1: Visualizar trapecios
n_vis = 6
x_vis = np.linspace(a, b, n_vis + 1)
y_vis = f(x_vis)
x_fine = np.linspace(a, b, 400)

axes[0].plot(x_fine, f(x_fine), 'k-', lw=2, label='f(x) exacta', zorder=3)
for i in range(n_vis):
    axes[0].fill([x_vis[i], x_vis[i], x_vis[i+1], x_vis[i+1]],
                 [0, y_vis[i], y_vis[i+1], 0], alpha=0.35, color='steelblue')
    axes[0].plot([x_vis[i], x_vis[i+1]], [y_vis[i], y_vis[i+1]], 'b--', lw=1)
axes[0].set_title(f"Trapecio (n={n_vis})\nI ≈ {trapecio(f,a,b,n_vis):.5f}")
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].legend()
axes[0].grid(True, ls='--', alpha=0.5)

# Panel 2: Visualizar parábolas de Simpson (n=6)
axes[1].plot(x_fine, f(x_fine), 'k-', lw=2, label='f(x) exacta', zorder=3)
for i in range(0, n_vis, 2):          # cada par de subintervalos
    xi = x_vis[i:i+3]
    yi = y_vis[i:i+3]
    # Coeficientes de la parábola que pasa por los 3 puntos
    coef = np.polyfit(xi, yi, 2)
    x_par = np.linspace(xi[0], xi[2], 80)
    axes[1].fill_between(x_par, np.polyval(coef, x_par), alpha=0.35,
                         color='orangered')
    axes[1].plot(x_par, np.polyval(coef, x_par), 'r-', lw=1)
axes[1].set_title(f"Simpson (n={n_vis})\nI ≈ {simpson(f,a,b,n_vis):.5f}")
axes[1].set_xlabel("x")
axes[1].set_ylabel("f(x)")
axes[1].legend()
axes[1].grid(True, ls='--', alpha=0.5)

# Panel 3: Comparación de errores
axes[2].loglog(N_vals, err_trap, 'o-', color='steelblue', ms=5, lw=2, label='Trapecio  O(h²)')
axes[2].loglog(N_vals, err_simp, 's-', color='orangered', ms=5, lw=2, label='Simpson   O(h⁴)')
# Líneas de referencia de orden
h = (b-a)/N_vals
axes[2].loglog(N_vals, err_trap[5] * (h/h[5])**2, 'b:', lw=1.2, label='∝ h²')
axes[2].loglog(N_vals, err_simp[5] * (h/h[5])**4, 'r:', lw=1.2, label='∝ h⁴')
axes[2].set_xlabel("Número de subintervalos n")
axes[2].set_ylabel("Error absoluto")
axes[2].set_title("Comparación de errores vs n")
axes[2].legend(fontsize=9)
axes[2].grid(True, which='both', ls='--', alpha=0.5)

plt.tight_layout()
plt.savefig("02_trapecio_simpson.png", dpi=130)
plt.show()
print("Gráfica guardada: 02_trapecio_simpson.png")
print(f"\nTrapecio (n=20): {trapecio(f,a,b,20):.8f}  |  error: {abs(trapecio(f,a,b,20)-I_exacto):.2e}")
print(f"Simpson  (n=20): {simpson( f,a,b,20):.8f}  |  error: {abs(simpson( f,a,b,20)-I_exacto):.2e}")
print(f"Exacto        : {I_exacto:.8f}")
