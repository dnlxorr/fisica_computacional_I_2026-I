try:
    n = int(input("Ingrese un número entero positivo: "))

    if n <= 0:
        print("Error >_< ingresar un número entero positivo.")
    else:
        # Lista principal
        lista = list(range(1, n + 1))

        # Pares e impares usando comprensión de listas
        pares = [num for num in lista if num % 2 == 0]
        impares = [num for num in lista if num % 2 != 0]

        # Función para verificar si un número es primo
        def es_primo(num):
            if num < 2:
                return False
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    return False
            return True

        # Lista de primos
        primos = [num for num in lista if es_primo(num)]

        # Impresión
        print("Lista de números:", lista)
        print("Lista de primos:", primos)

        print("Números Pares:", pares)
        print("Números Impares:", impares)

        print("Cantidad de Pares:", len(pares))
        print("Cantidad de Impares:", len(impares))

except ValueError:
    print("Error 0_o Debe ingresar un número entero positivo")