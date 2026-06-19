import numpy as np
import matplotlib.pyplot as plt

# ==================================================
# ERRORES EN DERIVADAS
# FÍSICA COMPUTACIONAL I
# ==================================================

# ==================================================
# FUNCIÓN
# ==================================================

def f(x):
    return np.sin(x) * np.exp(-0.1*x)

# ==================================================
# DERIVADA EXACTA
# ==================================================

def df(x):
    return np.exp(-0.1*x) * (np.cos(x) - 0.1*np.sin(x))

# ==================================================
# PARÁMETROS
# ==================================================

h = 0.05

x = np.linspace(0, 10, 500)

# Punto de evaluación
x0 = 4

# ==================================================
# DERIVADA NUMÉRICA
# ==================================================

derivada_num = (f(x + h) - f(x)) / h

# ==================================================
# DERIVADA EXACTA
# ==================================================

derivada_exac = df(x)

# ==================================================
# COMPARACIÓN EN UN PUNTO
# ==================================================

valor_exacto = df(x0)

valor_computador = (f(x0 + h) - f(x0)) / h

error_abs = abs(valor_exacto - valor_computador)

error_rel = (error_abs / abs(valor_exacto)) * 100

# ==================================================
# INFORME EN CONSOLA
# ==================================================

print("\n" + "="*65)
print("           ANÁLISIS DE ERRORES EN DERIVADAS")
print("="*65)

print(f"\nValor de h utilizado: {h}")

print(f"\nPunto de evaluación: x = {x0}")

print("\nRESULTADOS")
print("-"*30)

print(f"Valor exacto         = {valor_exacto:.8f}")
print(f"Valor del computador = {valor_computador:.8f}")
print(f"Error absoluto       = {error_abs:.8f}")
print(f"Error relativo (%)   = {error_rel:.6f}")

print("\nTIPO DE ERROR")
print("-"*30)
print("Error de truncamiento")

# ==================================================
# GRÁFICA
# ==================================================

plt.figure(figsize=(10,6))

# Derivada exacta (punteada marrón claro)
plt.plot(
    x,
    derivada_exac,
    '--',
    color='#6D4C41',
    linewidth=3,
    label='Derivada exacta'
)

# Derivada numérica (marrón oscuro)
plt.plot(
    x,
    derivada_num,
    color='#A1887F',
    linewidth=3,
    label='Derivada numérica'
)

plt.title(
    "Comparación entre Derivada Exacta y Derivada Numérica",
    fontsize=14
)

plt.xlabel("x")
plt.ylabel("f'(x)")

plt.grid(True, alpha=0.3)

plt.legend()

plt.tight_layout()
plt.show()