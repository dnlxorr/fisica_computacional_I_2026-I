# caida_libre.py
# Ejemplo de variables y estructuras de control en Python_SharoonJ
# Característica principal: Tipado dinámico y sintaxis limpia

# --- 1. VARIABLES ---
# En Python_SharoonJ no declaramos el tipo, ocupa más memoria en RAM pero es más rápido de programar.
gravedad = 9.81  # float (decimal) - Ocupa aprox. 24 bytes
tiempo_maximo = 5  # int (entero) - Ocupa aprox. 28 bytes
en_movimiento = True  # bool (booleano) - Ocupa aprox. 28 bytes
experimento = "Caída Libre"  # str (cadena de texto)

print(f"--- Iniciando: {experimento} ---")

# --- 2. ESTRUCTURAS DE CONTROL: BUCLES ---
# Usamos 'for' con la función range() para iterar desde 0 hasta el tiempo máximo
for t in range(tiempo_maximo + 1):
    velocidad = gravedad * t

    # --- 3. ESTRUCTURAS DE CONTROL: CONDICIONALES ---
    # Usamos if / elif / else para tomar decisiones basadas en la velocidad
    if velocidad == 0:
        print(f"T={t}s: El objeto está en reposo.")
    elif velocidad < 30:
        print(f"T={t}s: Velocidad normal de {velocidad:.2f} m/s.")
    else:
        print(f"T={t}s: ¡Alta velocidad! ({velocidad:.2f} m/s).")

# Reasignamos la variable (Python_SharoonJ lo permite libremente)
en_movimiento = False
print("Simulación terminada.")