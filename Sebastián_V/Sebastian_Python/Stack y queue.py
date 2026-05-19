# =========================================
# 🔹 STACK (PILA)
# =========================================

class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.is_empty():
            print("El stack está vacío")
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            print("El stack está vacío")
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def show(self):
        print(self.data)


# =========================================
# 🔹 QUEUE (COLA)
# =========================================

class Queue:
    def __init__(self):
        self.data = []

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if self.is_empty():
            print("La queue está vacía")
            return None
        return self.data.pop(0)  # elimina el primero

    def front(self):
        if self.is_empty():
            print("La queue está vacía")
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

    def show(self):
        print(self.data)


# =========================================
# 🔹 PRUEBA
# =========================================

if __name__ == "__main__":
    print("=== STACK ===")
    s = Stack()
    s.push(10)
    s.push("hola")
    s.push(3.14)
    s.show()

    print("Pop:", s.pop())
    print("Top:", s.peek())
    s.show()

    print("\n=== QUEUE ===")
    q = Queue()
    q.enqueue(1)
    q.enqueue("mundo")
    q.enqueue(2.5)
    q.show()

    print("Dequeue:", q.dequeue())
    print("Front:", q.front())
    q.show()