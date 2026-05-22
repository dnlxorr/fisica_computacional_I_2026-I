"""
INTEGRACIÓN NUMÉRICA II: Selección del número de pasos y Método de Romberg
Función de prueba: f(x) = x²·e^(-x)  en [0, 5]  (misma que el archivo anterior)
"""

import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**2 * np.exp(-x)

a, b = 0, 5
I_exacto = (-np.exp(-b)*(b**2+2*b+2)) - (-np.exp(-a)*(a**2+2*a+2))

# ─────────────────────────────────────────────────────────────
# REGLA DEL TRAPECIO (necesaria para Romberg)
# ─────────────────────────────────────────────────────────────
def trapecio(f, a, b, n):
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return h * (y[0]/2 + np.sum(y[1:-1]) + y[-1]/2)

# ─────────────────────────────────────────────────────────────
# SELECCIÓN DEL NÚMERO DE PASOS
# Estrategia simple: empieza con n=2 y duplica hasta que el cambio
# relativo entre dos estimaciones consecutivas sea menor que la tolerancia.
# No necesitamos saber cuántos pasos hacen falta de antemano.
# ─────────────────────────────────────────────────────────────
def seleccion_pasos(f, a, b, tol=1e-6):
    n = 2
    I_ant = trapecio(f, a, b, n)
    historia_n = [n]
    historia_I = [I_ant]
    while n <= 2**14:
        n *= 2
        I_act = trapecio(f, a, b, n)
        historia_n.append(n)
        historia_I.append(I_act)
        if abs(I_act - I_ant) / abs(I_act) < tol:
            break
        I_ant = I_act
    return np.array(historia_n), np.array(historia_I)

# ─────────────────────────────────────────────────────────────
# MÉTODO DE ROMBERG
# Construye una tabla triangular R[i][j] donde:
#   Columna 0: trapecio con 2^i subintervalos
#   Columna j: extrapolación de Richardson aplicada a la columna j-1
#
# ¿Por qué funciona la extrapolación de Richardson?
# El trapecio tiene error: I_trap = I_exacto + c₂·h² + c₄·h⁴ + ...
# Si calculamos con h y h/2:
#   I(h)   = I_exacto + c₂·h²    + c₄·h⁴   + ...
#   I(h/2) = I_exacto + c₂·h²/4  + c₄·h⁴/16 + ...
# Combinando: R = (4·I(h/2) - I(h)) / 3  → cancela el término c₂·h²
# Esto deja error O(h⁴). Repitiendo el proceso → O(h⁶), O(h⁸)...
# Fórmula general: R[i][j] = (4^j·R[i][j-1] - R[i-1][j-1]) / (4^j - 1)
# ─────────────────────────────────────────────────────────────
def romberg(f, a, b, orden=6):
    m = orden + 1
    R = np.zeros((m, m))
    for i in range(m):
        R[i, 0] = trapecio(f, a, b, 2**i)
        for j in range(1, i + 1):
            R[i, j] = (4**j * R[i, j-1] - R[i-1, j-1]) / (4**j - 1)
    return R

# ─────────────────────────────────────────────────────────────
# Ejecutar
# ─────────────────────────────────────────────────────────────
ns, Is = seleccion_pasos(f, a, b, tol=1e-8)
R = romberg(f, a, b, orden=6)

print("Tabla de Romberg:")
print(f"{'':>5}", end="")
for j in range(7): print(f"  j={j}       ", end="")
print()
for i in range(7):
    print(f"i={i} |", end="")
    for j in range(i+1):
        print(f"  {R[i,j]:.7f}", end="")
    print()

# ─────────────────────────────────────────────────────────────
# GRÁFICAS
# ─────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(13, 5))
fig.suptitle("Integración Numérica II — Romberg & Selección de pasos\n"
             f"f(x) = x²·e⁻ˣ,  I_exacto = {I_exacto:.7f}", fontsize=13, fontweight='bold')

# Panel 1: Selección de pasos
err_adap = np.abs(Is - I_exacto)
axes[0].loglog(ns, err_adap, 'D-', color='darkorange', ms=8, lw=2)
for n, e in zip(ns, err_adap):
    axes[0].annotate(f"n={n}", xy=(n, e), textcoords='offset points',
                     xytext=(5, 4), fontsize=7)
axes[0].axhline(1e-8, color='gray', ls='--', lw=1.5, label='Tolerancia 1e-8')
axes[0].set_xlabel("Número de subintervalos n")
axes[0].set_ylabel("Error absoluto")
axes[0].set_title("Selección adaptativa de pasos\n(duplicando n hasta converger)")
axes[0].legend()
axes[0].grid(True, which='both', ls='--', alpha=0.5)

# Panel 2: Convergencia de columnas de Romberg
colores = plt.cm.plasma(np.linspace(0.1, 0.85, 7))
for j in range(7):
    filas = np.arange(j, 7)
    errs  = [abs(R[i, j] - I_exacto) for i in filas]
    # Filtramos errores cero (para evitar log(0))
    errs_plot = [e if e > 1e-16 else 1e-16 for e in errs]
    label = f"Col j={j}  O(h^{2*(j+1)})"
    axes[1].semilogy(filas, errs_plot, 'o-', color=colores[j], ms=6, lw=1.8, label=label)

axes[1].set_xlabel("Fila i  (n = 2ⁱ subintervalos en col. 0)")
axes[1].set_ylabel("Error absoluto")
axes[1].set_title("Tabla de Romberg: cada columna\nelimina un orden de error más")
axes[1].legend(fontsize=7.5)
axes[1].grid(True, which='both', ls='--', alpha=0.5)

plt.tight_layout()
plt.savefig("03_romberg.png", dpi=130)
plt.show()
print("Gráfica guardada: 03_romberg.png")
