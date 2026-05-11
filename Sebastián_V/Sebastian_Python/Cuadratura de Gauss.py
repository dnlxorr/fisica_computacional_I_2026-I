import numpy as np
from scipy.integrate import fixed_quad

# Definir la función a integrar
def f(x):
    return x**2

# Intervalo de integración
a, b = 0, 2

# Aplicar cuadratura de Gauss (n=2 puntos)
resultado, _ = fixed_quad(f, a, b, n=2)

print(f"Resultado con cuadratura de Gauss: {resultado:.4f}")
print(f"Valor exacto: 8/3 ≈ {8/3:.4f}")
print(f"Error absoluto: {abs(resultado - 8/3):.6f}")
