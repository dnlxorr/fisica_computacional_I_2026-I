"""
INTEGRACIÓN NUMÉRICA IV: Intervalos infinitos e Integrales múltiples
Funciones de prueba:
  - Intervalo infinito: f(x) = e^(-x²)  en [0, ∞)  → valor exacto = √π/2
  - Integral doble:     g(x,y) = e^(-x²-y²)  en [0,∞)×[0,∞) → valor exacto = π/4
Estas son las integrales gaussianas, fundamentales en física estadística.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate as sci_int

# ─────────────────────────────────────────────────────────────
# INTEGRAL EN INTERVALO INFINITO
# f(x) = e^(-x²),  ∫₀^∞ e^(-x²) dx = √π/2 ≈ 0.8862
#
# Estrategia: cambio de variable t = 1/(1+x) → x = 1/t - 1
#   cuando x→∞, t→0; cuando x=0, t=1
#   dx = -1/t² dt
#   ∫₀^∞ f(x) dx = ∫₀^1 f(1/t - 1) · (1/t²) dt
# Esto convierte el límite infinito en el intervalo FINITO [0,1]
# que sí podemos integrar con Gauss-Legendre o Trapecio.
# ─────────────────────────────────────────────────────────────
def f_inf(x):
    return np.exp(-x**2)

I_inf_exacto = np.sqrt(np.pi) / 2   # valor exacto

def cambio_variable(t):
    """f transformada: t ∈ (0,1] → x = 1/t - 1 ∈ [0,∞)"""
    t = np.atleast_1d(np.array(t, dtype=float))
    result = np.zeros_like(t)
    mask = t > 1e-12
    x = 1.0/t[mask] - 1
    result[mask] = f_inf(x) / t[mask]**2
    return result

def gauss(f, a, b, n):
    t_i, w_i = np.polynomial.legendre.leggauss(n)
    x_i = 0.5*(b-a)*t_i + 0.5*(b+a)
    return 0.5*(b-a) * np.dot(w_i, f(x_i))

def trapecio(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b-a)/n
    return h*(y[0]/2 + np.sum(y[1:-1]) + y[-1]/2)

# Comparar métodos para la integral infinita
N_vals = np.arange(4, 60, 4)
err_gauss_inf = [abs(gauss(   cambio_variable, 1e-10, 1, n) - I_inf_exacto) for n in N_vals]
err_trap_inf  = [abs(trapecio(cambio_variable, 1e-10, 1, n) - I_inf_exacto) for n in N_vals]

# Corte artificial en límite grande (sin cambio de variable) — para comparar
err_corte = []
for L in [2, 4, 6, 8, 10]:
    I_corte = gauss(f_inf, 0, L, 20)
    err_corte.append(abs(I_corte - I_inf_exacto))

# ─────────────────────────────────────────────────────────────
# INTEGRAL DOBLE
# g(x,y) = e^(-x²-y²),  ∫₀^∞∫₀^∞ e^(-x²-y²) dx dy = π/4
# Aquí la truncamos en [0,L]×[0,L] con L=4 (el error es despreciable)
# Método: producto tensorial de Gauss en x e y
#   ∫∫ g dA ≈ Σᵢ Σⱼ wᵢ·wⱼ · g(xᵢ, yⱼ) · (Δx/2)·(Δy/2)
# ─────────────────────────────────────────────────────────────
def integral_doble_gauss(n, L=4):
    t_i, w_i = np.polynomial.legendre.leggauss(n)
    xi = 0.5*L*t_i + 0.5*L
    # Producto tensorial: grilla de nodos en 2D
    X, Y = np.meshgrid(xi, xi)
    W    = np.outer(w_i, w_i)
    return (0.5*L)**2 * np.sum(W * np.exp(-X**2 - Y**2))

I_doble_exacto = np.pi / 4
N_doble = np.arange(2, 25)
err_doble = [abs(integral_doble_gauss(n) - I_doble_exacto) for n in N_doble]

# ─────────────────────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Integración Numérica IV — Intervalos infinitos e Integrales múltiples",
             fontsize=13, fontweight='bold')

# Panel 1: f(x) = e^(-x²) con área bajo la curva
x_plot = np.linspace(0, 5, 400)
axes[0].fill_between(x_plot, f_inf(x_plot), alpha=0.3, color='teal',
                     label=f'Área = √π/2 ≈ {I_inf_exacto:.4f}')
axes[0].plot(x_plot, f_inf(x_plot), 'k-', lw=2)
axes[0].axvline(4, color='red', ls='--', lw=1.5, label='Corte en x=4\n(error despreciable)')
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].set_title("f(x) = e^(-x²)  en [0, ∞)\nIntegral gaussiana")
axes[0].legend(fontsize=8)
axes[0].grid(True, ls='--', alpha=0.5)

# Panel 2: Convergencia para la integral infinita
axes[1].semilogy(N_vals, err_gauss_inf, 'D-', color='darkorchid', ms=6, lw=2,
                 label='Gauss + cambio de variable')
axes[1].semilogy(N_vals, err_trap_inf,  'o-', color='steelblue',  ms=5, lw=2,
                 label='Trapecio + cambio de variable')
axes[1].semilogy([2,4,6,8,10], err_corte, 'rs--', ms=6, lw=1.5,
                 label='Gauss con corte en L\n(sin cambio de variable)')
axes[1].set_xlabel("n puntos / subintervalos")
axes[1].set_ylabel("Error absoluto")
axes[1].set_title("Integral en [0,∞): cambio de variable\nvs corte artificial en L")
axes[1].legend(fontsize=8)
axes[1].grid(True, which='both', ls='--', alpha=0.5)

# Panel 3: Integral doble — convergencia y superficie
ax3a = axes[2]
ax3a.semilogy(N_doble, err_doble, 's-', color='darkorange', ms=6, lw=2)
ax3a.set_xlabel("n puntos por dimensión")
ax3a.set_ylabel("Error absoluto")
ax3a.set_title(f"Integral doble: ∫∫ e^(-x²-y²) dA\nExacto = π/4 ≈ {I_doble_exacto:.6f}")
ax3a.grid(True, which='both', ls='--', alpha=0.5)
# Anotar cuántos puntos para error < 1e-8
for ni, ei in zip(N_doble, err_doble):
    if ei < 1e-8:
        ax3a.axvline(ni, color='red', ls='--', lw=1.2)
        ax3a.text(ni+0.3, 1e-7, f"n={ni}\nerror<1e-8", color='red', fontsize=8)
        break

# Mini inserción: superficie g(x,y)
ax_ins = fig.add_axes([0.72, 0.35, 0.22, 0.35], projection='3d')
xp = np.linspace(0, 3, 40)
yp = np.linspace(0, 3, 40)
Xg, Yg = np.meshgrid(xp, yp)
Zg = np.exp(-Xg**2 - Yg**2)
ax_ins.plot_surface(Xg, Yg, Zg, cmap='plasma', alpha=0.85)
ax_ins.set_xlabel("x", fontsize=7)
ax_ins.set_ylabel("y", fontsize=7)
ax_ins.set_title("g(x,y)", fontsize=8)
ax_ins.tick_params(labelsize=6)

plt.tight_layout()
plt.savefig("05_integrales_especiales.png", dpi=130)
plt.show()
print("Gráfica guardada: 05_integrales_especiales.png")
print(f"\nIntegral infinita con cambio de variable (n=20): {gauss(cambio_variable, 1e-10, 1, 20):.10f}")
print(f"Exacto √π/2                                     : {I_inf_exacto:.10f}")
print(f"\nIntegral doble Gauss (n=10): {integral_doble_gauss(10):.10f}")
print(f"Exacto π/4               : {I_doble_exacto:.10f}")
