# estructuras_mixtas.py
# Stack y Queue con datos mixtos en Python

# STACK (PILA)

class Stack:
    def __init__(self):
        self.elementos = []

    def push(self, valor):
        self.elementos.append(valor)

    def pop(self):
        if len(self.elementos) == 0:
            return None
        return self.elementos.pop()

    def peek(self):
        if len(self.elementos) == 0:
            return None
        return self.elementos[-1]

# QUEUE (COLA)

class Queue:
    def __init__(self):
        self.elementos = []

    def enqueue(self, valor):
        self.elementos.append(valor)

    def dequeue(self):
        if len(self.elementos) == 0:
            return None
        return self.elementos.pop(0)  # elimina el primero

    def front(self):
        if len(self.elementos) == 0:
            return None
        return self.elementos[0]

# MAIN (PRUEBAS)

# -------- STACK --------
pila = Stack()

pila.push(10)
pila.push("hola")
pila.push(3.14)
pila.push(True)

print("Stack completo:", pila.elementos)
print("Cima del stack:", pila.peek())

pila.pop()
print("Después de pop:", pila.elementos)

# -------- QUEUE --------
cola = Queue()

cola.enqueue(1)
cola.enqueue("mundo")
cola.enqueue(2.71)
cola.enqueue(False)

print("\nQueue completa:", cola.elementos)
print("Frente de la cola:", cola.front())

cola.dequeue()
print("Después de dequeue:", cola.elementos)