# =====================
# PILA (STACK)
# =====================
class Pila:
    def __init__(self):
        self.datos = []

    def agregar(self, item):
        self.datos.append(item)

    def quitar(self):
        if self.vacia():
            return None
        return self.datos.pop()

    def cima(self):
        if self.vacia():
            return None
        return self.datos[-1]

    def vacia(self):
        return len(self.datos) == 0


# =====================
# COLA (QUEUE)
# =====================
class Cola:
    def __init__(self):
        self.datos = []

    def insertar(self, item):
        self.datos.append(item)

    def extraer(self):
        if self.vacia():
            return None
        return self.datos.pop(0)

    def primero(self):
        if self.vacia():
            return None
        return self.datos[0]

    def vacia(self):
        return len(self.datos) == 0


# =====================
# PRUEBAS
# =====================
def ejecutar_pruebas():

    # -------- PILA --------
    mi_pila = Pila()

    mi_pila.agregar(10)
    mi_pila.agregar("hola")
    mi_pila.agregar(3.14)
    mi_pila.agregar(True)

    print("Contenido de la pila:", mi_pila.datos)
    print("Elemento en la cima:", mi_pila.cima())

    mi_pila.quitar()
    print("Después de quitar:", mi_pila.datos)

    # -------- COLA --------
    mi_cola = Cola()

    mi_cola.insertar(1)
    mi_cola.insertar("mundo")
    mi_cola.insertar(2.71)
    mi_cola.insertar(False)

    print("\nContenido de la cola:", mi_cola.datos)
    print("Primer elemento:", mi_cola.primero())

    mi_cola.extraer()
    print("Después de extraer:", mi_cola.datos)


if __name__ == "__main__":
    ejecutar_pruebas()