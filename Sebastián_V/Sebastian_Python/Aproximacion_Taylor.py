import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------
# 1) Aproximaciones
# -----------------------------------
def taylor_4(x):
    return (np.exp(x) +
            (np.exp(3*x))/6 +
            (np.exp(5*x))/120 +
            (np.exp(7*x))/5040)

def taylor_7(x):
    return (np.exp(x) +
            (np.exp(3*x))/6 +
            (np.exp(5*x))/120 +
            (np.exp(7*x))/5040 +
            (np.exp(9*x))/362880 +
            (np.exp(11*x))/39916800 +
            (np.exp(13*x))/6227020800)

# -----------------------------------
# 2) Datos
# -----------------------------------
x = np.linspace(-2.0, 2.0, 500)

y4 = taylor_4(x)
y7 = taylor_7(x)

# -----------------------------------
# 3) Error cuadrático medio
# -----------------------------------
mse = np.mean((y4 - y7)**2)

# -----------------------------------
# 4) Gráfica
# -----------------------------------
plt.figure(figsize=(10,6))

plt.plot(x, y7, label="Taylor 7 términos", linewidth=2)
plt.plot(x, y4, '--', label="Taylor 4 términos", linewidth=2)

# Mostrar el MSE dentro de la gráfica
plt.text(0.05, 0.95,
         f"MSE = {mse:.2e}",
         transform=plt.gca().transAxes,
         fontsize=12,
         verticalalignment='top',
         bbox=dict())

# Decoración
plt.title("Aproximación de Taylor de sinh(e^x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid()

plt.show()