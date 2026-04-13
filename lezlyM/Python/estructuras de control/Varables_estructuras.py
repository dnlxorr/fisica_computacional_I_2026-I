
nombre_tienda = "Coffee"
abierto = True
precio_base = 2.50
capacidad_maxima = 50


menu = ["Espresso", "Latte", "Capuchino"]
stock = {
    "granos": 10,
    "leche": 5,
    "vasos": 100
}



print(f"--- Bienvenidos a {nombre_tienda} ---")


if abierto and stock["granos"] > 0:
    print("Estado: Estamos listos para atenderte.")


    print("\nNuestro menú de hoy:")
    for indice, cafe in enumerate(menu, 1):

        precio_actual = precio_base + indice
        print(f"{indice}. {cafe} - ${precio_actual}")

else:
    print("Estado: Lo sentimos, estamos cerrados o sin suministros.")


clientes_esperando = 3
print("\nAtendiendo fila...")

while clientes_esperando > 0:
    print(f"Sirviendo café... Quedan {clientes_esperando} personas.")


print("¡Fila terminada!")