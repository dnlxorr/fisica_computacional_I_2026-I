# ----------------------------------------------------------
# ERROR EN INTEGRACIÓN NUMÉRICA
# ----------------------------------------------------------
# Este programa calcula el error absoluto.
#
# Fórmula:
#
# Error = |Valor real - Valor aproximado|
# ----------------------------------------------------------

# Valor real de la integral
valor_real = 8.3333

# Valor aproximado
valor_aproximado = 8.5

# abs() calcula valor absoluto
# Elimina signos negativos
error = abs(valor_real - valor_aproximado)

print("El error absoluto es:", error)