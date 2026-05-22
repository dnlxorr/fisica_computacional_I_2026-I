"""
INTEGRACIÓN NUMÉRICA III: Cuadratura de Gauss-Legendre
Función de prueba: f(x) = x²·e^(-x)  en [0, 5]
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2 * np.exp(-x)

a, b = 0, 5
I_exacto = (-np.exp(-b)*(b**2+2*b+2)) - (-np.exp(-a)*(a**2+2*a+2))

def trapecio(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2)

def simpson(f, a, b, n):
    if n % 2 != 0: n += 1
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h/3 * (y[0] + 4*np.sum(y[1:-1:2]) + 2*np.sum(y[2:-2:2]) + y[-1])

# ─────────────────────────────────────────────────────────────
# CUADRATURA DE GAUSS-LEGENDRE
# En lugar de nodos equiespaciados, elige n nodos y pesos óptimos
# que integran exactamente polinomios de grado hasta 2n-1.
# Los nodos son las raíces del polinomio de Legendre Pₙ(t) en [-1,1].
#
# Transformación de [-1,1] → [a,b]:
#   x = (b-a)/2 · t + (a+b)/2
#   dx = (b-a)/2 · dt
# Por eso el resultado se multiplica por (b-a)/2.
# ─────────────────────────────────────────────────────────────
def gauss(f, a, b, n):
    # np.polynomial.legendre.leggauss devuelve nodos tᵢ y pesos wᵢ en [-1,1]
    t_i, w_i = np.polynomial.legendre.leggauss(n)
    # Cambio de variable al intervalo [a, b]
    x_i = 0.5 * (b - a) * t_i + 0.5 * (b + a)
    return 0.5 * (b - a) * np.dot(w_i, f(x_i))

# ─────────────────────────────────────────────────────────────
# Errores para distintos n
# ─────────────────────────────────────────────────────────────
N_vals = np.arange(2, 30)
err_trap  = [abs(trapecio(f, a, b, n) - I_exacto) for n in N_vals]
err_simp  = [abs(simpson( f, a, b, n) - I_exacto) for n in N_vals]
err_gauss = [abs(gauss(   f, a, b, n) - I_exacto) for n in N_vals]

# ─────────────────────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Integración Numérica III — Gauss-Legendre\n"
             f"f(x) = x²·e⁻ˣ,  I_exacto = {I_exacto:.7f}", fontsize=13, fontweight='bold')

# Panel 1: Nodos de Gauss sobre la función (n=8)
n_vis = 8
t_i, w_i = np.polynomial.legendre.leggauss(n_vis)
x_i = 0.5*(b-a)*t_i + 0.5*(b+a)
y_i = f(x_i)
x_fine = np.linspace(a, b, 400)

axes[0].fill_between(x_fine, f(x_fine), alpha=0.15, color='darkorchid')
axes[0].plot(x_fine, f(x_fine), 'k-', lw=2, label='f(x) exacta')
# Tamaño de cada nodo proporcional a su peso wᵢ
axes[0].scatter(x_i, y_i, s=300 * w_i / w_i.max(), color='darkorchid',
                zorder=5, label=f'Nodos Gauss (n={n_vis})\ntamaño ∝ peso wᵢ')
axes[0].vlines(x_i, 0, y_i, color='darkorchid', lw=1, ls='--', alpha=0.5)
# Comparar con nodos equiespaciados
x_eq = np.linspace(a, b, n_vis)
axes[0].scatter(x_eq, f(x_eq), s=60, marker='x', color='red',
                zorder=5, label=f'Nodos equiespaciados (n={n_vis})', linewidths=2)
axes[0].set_xlabel("x")
axes[0].set_ylabel("f(x)")
axes[0].set_title(f"Nodos de Gauss vs Nodos equiespaciados\n"
                  f"Gauss: I ≈ {gauss(f,a,b,n_vis):.7f}")
axes[0].legend(fontsize=8)
axes[0].grid(True, ls='--', alpha=0.5)

# Panel 2: Comparación de errores
axes[1].semilogy(N_vals, err_trap,  'o-', color='steelblue', ms=5, lw=2, label='Trapecio')
axes[1].semilogy(N_vals, err_simp,  's-', color='orangered',  ms=5, lw=2, label='Simpson')
axes[1].semilogy(N_vals, err_gauss, 'D-', color='darkorchid', ms=5, lw=2, label='Gauss-Legendre')
axes[1].set_xlabel("Número de puntos / subintervalos n")
axes[1].set_ylabel("Error absoluto")
axes[1].set_title("Gauss converge mucho más rápido\ncon los mismos n puntos")
axes[1].legend()
axes[1].grid(True, which='both', ls='--', alpha=0.5)

# Anotar cuántos puntos necesita cada método para error < 1e-8
tol = 1e-8
for errs, nombre, color in [(err_trap,'Trapecio','steelblue'),
                             (err_simp,'Simpson','orangered'),
                             (err_gauss,'Gauss','darkorchid')]:
    for ni, ei in zip(N_vals, errs):
        if ei < tol:
            axes[1].axvline(ni, color=color, ls=':', lw=1.2, alpha=0.7)
            axes[1].text(ni+0.3, tol*3, f"n={ni}", color=color, fontsize=8)
            break
axes[1].axhline(tol, color='gray', ls='--', lw=1, label='tol=1e-8')
axes[1].legend(fontsize=8)

plt.tight_layout()
plt.savefig("04_gauss.png", dpi=130)
plt.show()
print("Gráfica guardada: 04_gauss.png")
print(f"\nGauss n=5 : {gauss(f,a,b,5):.10f}  error: {abs(gauss(f,a,b,5)-I_exacto):.2e}")
print(f"Gauss n=10: {gauss(f,a,b,10):.10f}  error: {abs(gauss(f,a,b,10)-I_exacto):.2e}")
print(f"Exacto    : {I_exacto:.10f}")
