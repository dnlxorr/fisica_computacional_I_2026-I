from collections import deque

class StackQueue:
    def __init__(self):
        # Inicializamos el Deque
        self.datos = deque()

    # --- MÉTODOS DE STACK (PILA) ---
    def push(self, elemento):
        """Agrega un elemento al final de la estructura."""
        self.datos.append(elemento)

    def pop(self):
        """Saca y retorna el ÚLTIMO elemento que entró (LIFO)."""
        if self.datos:
            return self.datos.pop()
        return None

    # --- MÉTODOS DE QUEUE (COLA) ---
    def enqueue(self, elemento):
        """Agrega un elemento al final (hace la misma acción que push)."""
        self.datos.append(elemento)

    def dequeue(self):
        """Saca y retorna el PRIMER elemento que entró (FIFO)."""
        if self.datos:
            return self.datos.popleft()
        return None

    def mostrar(self):
        return list(self.datos)

# --- PRUEBA MEZCLANDO DATOS ---
mezclador = StackQueue()
mezclador.push("A")
mezclador.push("B")
mezclador.enqueue("C") # "C" entra al final de la fila

print(f"Estado actual: {mezclador.mostrar()}") # ['A', 'B', 'C']

# Usando comportamiento de Stack (saca el último: C)
print(f"Haciendo POP (Stack): {mezclador.pop()}")

# Usando comportamiento de Queue (saca el primero: A)
print(f"Haciendo DEQUEUE (Queue): {mezclador.dequeue()}")

print(f"Estado final: {mezclador.mostrar()}") # Solo queda ['B']