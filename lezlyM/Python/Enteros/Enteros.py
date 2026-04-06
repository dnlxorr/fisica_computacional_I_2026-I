def clasificar_numeros(n):
    pares = []
    impares = []
    primos = []

    for num in range(1, n + 1):
        # Clasificación de Pares e Impares
        if num % 2 == 0:
            pares.append(num)
        else:
            impares.append(num)

        # Clasificación de Primos
        if num > 1:
            es_primo = True
            for i in range(2, int(num ** 0.5) + 1):
                if num % i == 0:
                    es_primo = False
                    break
            if es_primo:
                primos.append(num)

    # Resultados
    print(f"--- Resultados hasta {n} ---")
    print(f"Pares ({len(pares)}): {pares}")
    print(f"Impares ({len(impares)}): {impares}")
    print(f"Primos ({len(primos)}): {primos}")


# Ejemplo de uso con n = 20
clasificar_numeros(20)