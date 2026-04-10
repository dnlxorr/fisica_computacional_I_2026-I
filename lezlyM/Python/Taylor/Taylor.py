import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# 1. Definición simbólica para la Serie de Taylor "automática"
x_sym = sp.Symbol('x')
a, b, c = 1, -2, 1
f_sym = a*x_sym**2 + b*x_sym + c

# Punto de expansión (a)
punto_a = 0.5

# Expansión automática con SymPy (grado 2)
taylor_auto_sym = sp.series(f_sym, x_sym, punto_a, 3).removeO()
taylor_auto_func = sp.lambdify(x_sym, taylor_auto_sym, 'numpy')

# 2. Definición numérica para gráficas
x_vals = np.linspace(-1, 3, 100)
f_original = a*x_vals**2 + b*x_vals + c

# Expansión manual (calculada en el paso anterior)
# f(a) + f'(a)(x-a) + (f''(a)/2)(x-a)^2
f_a = a*punto_a**2 + b*punto_a + c
df_a = 2*a*punto_a + b
ddf_a = 2*a
taylor_manual = f_a + df_a*(x_vals - punto_a) + (ddf_a/2)*(x_vals - punto_a)**2

# Taylor automática convertida a valores numéricos
taylor_auto_vals = taylor_auto_func(x_vals)

# 3. Cálculo del Error Cuadrático Medio (MSE)
# Como es una cuadrática, el error debería ser prácticamente cero (orden de 1e-16)
mse = np.mean((taylor_manual - taylor_auto_vals)**2)
print(f"Error Cuadrático Medio entre manual y automático: {mse}")

# 4. Graficación
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]})

# Gráfica principal
ax1.plot(x_vals, f_original, 'k-', linewidth=3, label='Función Original $f(x)$', alpha=0.3)
ax1.plot(x_vals, taylor_manual, 'r--', label='Taylor Manual')
ax1.plot(x_vals, taylor_auto_vals, 'b:', label='Taylor Automática (SymPy)')
ax1.scatter([punto_a], [f_a], color='green', zorder=5, label=f'Punto de expansión (x={punto_a})')

ax1.set_title('Comparación de Expansión de Taylor')
ax1.legend()
ax1.grid(True)

# Gráfica de error (Residuo)
error_diff = taylor_manual - taylor_auto_vals
ax2.plot(x_vals, error_diff, color='purple', label='Diferencia (Manual - Auto)')
ax2.set_ylabel('Diferencia')
ax2.set_xlabel('x')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()