pila = []

pila.append(10)
pila.append("hola")
pila.append(3.14)

sacado_pila = pila.pop()

cola = []

cola.append(100)
cola.append("mundo")
cola.append(9.81)

sacado_cola = cola.pop(0)


print("Pila:", pila)
print("Sacado de pila:", sacado_pila)

print("Cola:", cola)
print("Sacado de cola:", sacado_cola)