# ---------------------------------------------------
# EJEMPLO DE DIFERENCIAS FINITAS
# Función: f(x) = x²
# ---------------------------------------------------

# Definimos la función
def f(x):
    return x**2


# Punto donde queremos calcular la derivada
x = 2

# Tamaño del paso
h = 0.1

# DERIVADA EXACTA
derivada_exacta = 2 * x

# DIFERENCIA PROGRESIVA
derivada_progresiva = (f(x + h) - f(x)) / h

# DIFERENCIA REGRESIVA
derivada_regresiva = (f(x) - f(x - h)) / h

# DIFERENCIA CENTRADA
derivada_centrada = (f(x + h) - f(x - h)) / (2 * h)


# ---------------------------------------------------
# RESULTADOS
# ---------------------------------------------------

print("FUNCIÓN: f(x) = x²")
print("Punto evaluado: x =", x)
print("Paso utilizado: h =", h)

print("\n--- RESULTADOS ---")

print("Derivada exacta      =", derivada_exacta)
print("Diferencia progresiva =", derivada_progresiva)
print("Diferencia regresiva  =", derivada_regresiva)
print("Diferencia centrada   =", derivada_centrada)


# ---------------------------------------------------
# ERRORES
# ---------------------------------------------------

error_progresiva = abs(derivada_exacta - derivada_progresiva)
error_regresiva = abs(derivada_exacta - derivada_regresiva)
error_centrada = abs(derivada_exacta - derivada_centrada)

print("\n--- ERRORES ABSOLUTOS ---")

print("Error progresiva =", error_progresiva)
print("Error regresiva  =", error_regresiva)
print("Error centrada   =", error_centrada)