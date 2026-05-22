import numpy as np
import matplotlib.pyplot as plt

# Función a integrar
def f(x):
    return np.sin(x)

# Método del trapecio compuesto
def trapecio_compuesto(f, a, b, n):
    h = (b - a) / n
    suma = 0.5 * (f(a) + f(b))

    for i in range(1, n):
        suma += f(a + i*h)

    return h * suma

# Integración de Romberg
def romberg(f, a, b, niveles):

    # Crear matriz de Romberg
    R = np.zeros((niveles, niveles))

    # Primera columna: trapecio compuesto
    for k in range(niveles):

        n = 2**k

        R[k, 0] = trapecio_compuesto(f, a, b, n)

    # Extrapolación de Richardson
    for j in range(1, niveles):

        for k in range(j, niveles):

            R[k, j] = (
                (4**j * R[k, j-1] - R[k-1, j-1])
                / (4**j - 1)
            )

    return R

# Intervalo
a = 0
b = np.pi

# Número de niveles de Romberg
niveles = 6

# Calcular tabla de Romberg
R = romberg(f, a, b, niveles)

# Mostrar tabla
print("Tabla de Romberg:\n")

for i in range(niveles):

    for j in range(i + 1):

        print(f"{R[i,j]:.10f}", end="\t")

    print()

# Valor exacto
valor_exacto = 2

# Errores de la diagonal principal
errores = []

for i in range(niveles):

    errores.append(abs(valor_exacto - R[i, i]))

# -----------------------------
# Gráfica del error
# -----------------------------
plt.figure(figsize=(8,5))

plt.plot(range(1, niveles + 1), errores, 'o-')

plt.yscale('log')

plt.title('Convergencia de la integración de Romberg')
plt.xlabel('Nivel')
plt.ylabel('Error absoluto')
plt.grid(True)

plt.show()