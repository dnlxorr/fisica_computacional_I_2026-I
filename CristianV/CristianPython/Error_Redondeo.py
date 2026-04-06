# Método básico usando floats (números de punto flotante)
total = 0.0
for _ in range(1_000_000):
    total += 0.1
print(f"Resultado de sumar 0.1 un millón de veces: {total}")