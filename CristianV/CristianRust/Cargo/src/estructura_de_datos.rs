use std::collections::VecDeque;

// Definimos la estructura usando Generics <T>
struct StackQueue<T> {
    datos: VecDeque<T>,
}

impl<T> StackQueue<T> {
    // Constructor
    fn new() -> Self {
        StackQueue {
            datos: VecDeque::new(),
        }
    }

    // --- MÉTODOS DE STACK (PILA) ---
    fn push(&mut self, elemento: T) {
        // Agrega al final
        self.datos.push_back(elemento);
    }

    fn pop(&mut self) -> Option<T> {
        // Saca del final (LIFO)
        self.datos.pop_back()
    }

    // --- MÉTODOS DE QUEUE (COLA) ---
    fn enqueue(&mut self, elemento: T) {
        // En una cola, los datos entran por el mismo lado que en la pila
        self.datos.push_back(elemento);
    }

    fn dequeue(&mut self) -> Option<T> {
        // Saca del principio (FIFO)
        self.datos.pop_front()
    }
}

pub(crate) fn estructura() {
    let mut mezclador = StackQueue::new();

    // Mezclando el ingreso de datos
    mezclador.push(10);
    mezclador.push(20);
    mezclador.enqueue(30);

    // Salida usando ambos comportamientos
    // Saca el último (30)
    println!("Haciendo POP (Stack): {:?}", mezclador.pop().unwrap());
    // Saca el primero (10)
    println!("Haciendo DEQUEUE (Queue): {:?}", mezclador.dequeue().unwrap());
}