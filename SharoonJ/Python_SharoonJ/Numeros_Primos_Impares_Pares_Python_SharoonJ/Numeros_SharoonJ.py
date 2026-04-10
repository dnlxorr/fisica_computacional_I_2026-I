try:
    n = int(input("Ingrese un numero entero positivo: "))

    if n <= 0:
        print("Error >_< ingresar un numero entero positivo.")
    else:
        pares = []
        impares = []
        primos = []

        lista = list(range(1, n+1))

        for i in range(1, n + 1):

            # Pares e impares
            if i % 2 == 0:
                pares.append(i)
            else:
                impares.append(i)

        # Primos
        for i in range(2, n + 1):
            es_primo = True

            for j in range(2, i):
                if i % j == 0:
                    es_primo = False
                    break

            if es_primo:
                primos.append(i)

        # Impresión
        print("Lista de numeros:", lista)
        print("Lista de primos:", primos)

        print("Numeros Pares:", pares)
        print("Numeros Impares:", impares)

        print("Cantidad de Pares:", len(pares))
        print("Cantidad de Impares:", len(impares))

except ValueError:
    print("Error 0_o Debe ingresar un numero entero positivo")