def es_primo(num):
    if num < 2:
        return False
    for k in range(2, int(num**0.5) + 1):
        if num % k == 0:
            return False
    return True


try:
    numero = int(input("Digite un numero entero positivo: "))

    if numero <= 0:
        print("Error *_* El numero debe ser positivo.")
    else:
        lista_numeros = list(range(1, numero + 1))

        lista_pares = []
        lista_impares = []
        lista_primos = []

        for valor in lista_numeros:

            if valor % 2 == 0:
                lista_pares.append(valor)
            else:
                lista_impares.append(valor)

            if es_primo(valor):
                lista_primos.append(valor)

        print("Numeros generados:", lista_numeros)
        print("Numeros primos:", lista_primos)

        print("Pares:", lista_pares)
        print("Impares:", lista_impares)

        print("Total de pares:", len(lista_pares))
        print("Total de impares:", len(lista_impares))

except ValueError:
    print("Error >_< Debe ingresar un numero entero.")