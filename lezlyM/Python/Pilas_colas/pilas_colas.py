from collections import deque


pedidos = [
    {"id": 1, "producto": "Café", "precio": 2.5},
    {"id": 2, "producto": "Pan", "precio": 1.5},
    {"id": 3, "producto": "Té", "precio": 2.0}
]


cola = deque(pedidos)
pila = pedidos.copy()

print("--- 🛒 PROCESANDO VENTAS ---")


cliente_f = cola.popleft()
print(f"COLA (Primero): Atendiendo pedido {cliente_f['id']} de {cliente_f['producto']}")


cliente_p = pila.pop()
print(f"PILA (Último): Atendiendo pedido {cliente_p['id']} de {cliente_p['producto']}")