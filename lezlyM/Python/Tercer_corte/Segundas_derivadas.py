import numpy as np
import matplotlib.pyplot as plt

# ── Función de segunda derivada ──
def d2_centrada(f, x, h=1e-4):
    return (f(x+h)-2*f(x)+f(x-h))/h**2

# ── Prueba con sin(x) ────────────
x = np.linspace(-np.pi, np.pi, 200)
h = 0.1
f  = np.sin
d2 = np.array([d2_centrada(f,xi,h)
               for xi in x])

exacta = -np.sin(x)   # = f''(x)
error  = np.abs(d2 - exacta)
print(f'Error max: {error.max():.2e}')


# ── Graficar resultados ──────────
fig, axes = plt.subplots(1, 2)

axes[0].plot(x, d2,     label='Numérica')
axes[0].plot(x, exacta, label='Exacta',
             linestyle='--')
axes[0].set_title("f''(x)")
axes[0].legend()

axes[1].semilogy(x, error,
                 color='red')
axes[1].set_title('Error puntual')
axes[1].set_xlabel('x')

plt.tight_layout()
plt.show()
