import numpy as np
import matplotlib.pyplot as plt

# Valores de x
x = np.linspace(-2, 2, 100)

# Función real
y = np.exp(x)

# Aproximación de Taylor (3 términos)
t3 = 1 + x + (x**2)/2

# Aproximación de Taylor (6 términos)
t6 = 1 + x + (x**2)/2 + (x**3)/6 + (x**4)/24 + (x**5)/120

# Gráfica
plt.figure()
plt.plot(x, y, label="e^x (real)")
plt.plot(x, t3, label="Taylor 3 términos")
plt.plot(x, t6, label="Taylor 6 términos")

plt.title("Aproximación de e^x con Series de Taylor")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid()

plt.show()

# Error cuadrático medio
ecm_t3 = np.mean((y - t3)**2)
ecm_t6 = np.mean((y - t6)**2)

print("ECM (3 términos):", ecm_t3)
print("ECM (6 términos):", ecm_t6)