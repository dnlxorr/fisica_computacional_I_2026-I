import numpy as np

# Función de prueba y su derivada exacta
def f1(x):
    return x**3 - 2*x + 1

def df1(x):
    return 3*x**2 - 2

# Esquemas numéricos
def forward_diff(f, x, h):
    return (f(x + h) - f(x)) / h

def central_diff(f, x, h):
    return (f(x + h) - f(x - h)) / (2 * h)

# Demostración: cálculo de errores para distintos h
x = 1.5
h_vals = np.logspace(-6, -1, 6)
exacta = df1(x)

print("===== ERRORES EN LA DERIVACIÓN NUMÉRICA =====")
print(f"Derivada exacta en x = {x}: {exacta:.6f}\n")
print("   h        Error (adelante)   Error (central)")
for h in h_vals:
    fd = forward_diff(f1, x, h)
    cd = central_diff(f1, x, h)
    err_fd = abs(fd - exacta)
    err_cd = abs(cd - exacta)
    print(f" {h:.1e}      {err_fd:.2e}           {err_cd:.2e}")