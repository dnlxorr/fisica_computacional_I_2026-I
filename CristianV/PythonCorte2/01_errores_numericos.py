"""
ERRORES NUMÉRICOS: Redondeo, Truncamiento y Series de Taylor
Función de prueba: f(x) = sin(x)
- Conocemos los valores exactos de sin, cos → podemos calcular errores reales
"""

import numpy as np
import matplotlib.pyplot as plt

x0 = np.pi / 4  # punto donde evaluamos: sin(π/4) = √2/2

# ─────────────────────────────────────────────────────────────
# 1. ERROR DE REDONDEO
# Se da cuando usamos diferencias finitas para calcular derivadas.
# La derivada exacta de sin(x) es cos(x).
# La derivada numérica es: [f(x+h) - f(x)] / h
# Si h es muy pequeño → la computadora pierde dígitos significativos
# ─────────────────────────────────────────────────────────────
h_vals = np.logspace(-1, -15, 100)
derivada_exacta = np.cos(x0)
err_redondeo = []

for h in h_vals:
    derivada_num = (np.sin(x0 + h) - np.sin(x0)) / h
    err_redondeo.append(abs(derivada_num - derivada_exacta))

# ─────────────────────────────────────────────────────────────
# 2. ERROR DE TRUNCAMIENTO
# La serie de Taylor de sin(x) alrededor de 0 es:
#   sin(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
# Al cortar en el término N-ésimo se comete un error que decrece con N
# ─────────────────────────────────────────────────────────────
x_test = np.pi / 3  # evaluamos sin(π/3) = √3/2
valor_exacto = np.sin(x_test)
N_terms = range(1, 12, 2)   # 1, 3, 5, 7, 9, 11 términos
err_truncamiento = []
aproximaciones   = []

suma = 0.0
for n in range(1, 13, 2):
    import math
    suma += ((-1)**((n-1)//2)) * x_test**n / math.factorial(n)
    if n in N_terms:
        err_truncamiento.append(abs(suma - valor_exacto))
        aproximaciones.append(suma)

# ─────────────────────────────────────────────────────────────
# 3. SERIE DE TAYLOR de sin(x) alrededor de x0 = 0
#   Orden 1: sin(x) ≈ x
#   Orden 3: sin(x) ≈ x - x³/6
#   Orden 5: sin(x) ≈ x - x³/6 + x⁵/120
# ─────────────────────────────────────────────────────────────
x = np.linspace(-np.pi, np.pi, 400)
taylor1 = x
taylor3 = x - x**3 / 6
taylor5 = x - x**3 / 6 + x**5 / 120

# ─────────────────────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle("Errores Numéricos — f(x) = sin(x)", fontsize=14, fontweight='bold')

# Panel 1: Error de redondeo
axes[0].loglog(h_vals, err_redondeo, 'b-', lw=2)
axes[0].set_xlabel("Paso h")
axes[0].set_ylabel("Error absoluto")
axes[0].set_title("Error de Redondeo\n(derivada por diferencias finitas)")
axes[0].grid(True, which='both', ls='--', alpha=0.6)
h_opt = h_vals[np.argmin(err_redondeo)]
axes[0].axvline(h_opt, color='red', ls='--', label=f'h óptimo ≈ {h_opt:.1e}')
axes[0].legend(fontsize=8)
# Anotación explicativa
axes[0].text(0.05, 0.15, "← h muy pequeño:\ncancelación numérica",
             transform=axes[0].transAxes, fontsize=7, color='red')
axes[0].text(0.55, 0.85, "h muy grande →\nerror de truncamiento",
             transform=axes[0].transAxes, fontsize=7, color='navy')

# Panel 2: Error de truncamiento
axes[1].semilogy(list(N_terms), err_truncamiento, 'ro-', ms=8, lw=2)
for i, (n, e) in enumerate(zip(N_terms, err_truncamiento)):
    axes[1].annotate(f"N={n}\n{e:.1e}", xy=(n, e),
                     textcoords='offset points', xytext=(6, 4), fontsize=7)
axes[1].set_xlabel("Número de términos N")
axes[1].set_ylabel("Error absoluto")
axes[1].set_title("Error de Truncamiento\n(serie de Taylor de sin(x) en x=π/3)")
axes[1].grid(True, which='both', ls='--', alpha=0.6)

# Panel 3: Series de Taylor
axes[2].plot(x, np.sin(x), 'k-', lw=2.5, label='sin(x) exacto')
axes[2].plot(x, taylor1,  '--',  lw=1.5, label='Orden 1: x')
axes[2].plot(x, taylor3,  '-.',  lw=1.5, label='Orden 3: x − x³/6')
axes[2].plot(x, taylor5,  ':',   lw=2,   label='Orden 5: + x⁵/120')
axes[2].set_ylim(-2, 2)
axes[2].set_xlabel("x [rad]")
axes[2].set_ylabel("f(x)")
axes[2].set_title("Series de Taylor alrededor de x=0")
axes[2].legend(fontsize=8)
axes[2].grid(True, ls='--', alpha=0.6)

plt.tight_layout()
plt.savefig("01_errores_numericos.png", dpi=130)
plt.show()
print("Gráfica guardada: 01_errores_numericos.png")
