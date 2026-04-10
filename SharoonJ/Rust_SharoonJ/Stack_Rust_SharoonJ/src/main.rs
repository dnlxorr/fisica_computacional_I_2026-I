use std::collections::VecDeque;

// ENUM para manejar datos mixtos
#[derive(Debug)]
enum Valor {
    Entero(i32),
    Texto(String),
    Decimal(f64),
    Booleano(bool),
}

// -------- STACK (PILA) --------
struct Stack {
    elementos: Vec<Valor>,
}

impl Stack {
    fn new() -> Self {
        Stack { elementos: Vec::new() }
    }

    fn push(&mut self, valor: Valor) {
        self.elementos.push(valor);
    }

    fn pop(&mut self) -> Option<Valor> {
        self.elementos.pop()
    }

    fn peek(&self) -> Option<&Valor> {
        self.elementos.last()
    }
}

// -------- QUEUE (COLA) --------
struct Queue {
    elementos: VecDeque<Valor>,
}

impl Queue {
    fn new() -> Self {
        Queue { elementos: VecDeque::new() }
    }

    fn enqueue(&mut self, valor: Valor) {
        self.elementos.push_back(valor);
    }

    fn dequeue(&mut self) -> Option<Valor> {
        self.elementos.pop_front()
    }

    fn front(&self) -> Option<&Valor> {
        self.elementos.front()
    }
}

// -------- MAIN --------
fn main() {

    // -------- STACK --------
    let mut pila = Stack::new();

    pila.push(Valor::Entero(10));
    pila.push(Valor::Texto(String::from("hola")));
    pila.push(Valor::Decimal(3.14));
    pila.push(Valor::Booleano(true));

    println!("Stack completo: {:?}", pila.elementos);
    println!("Cima del stack: {:?}", pila.peek());

    pila.pop();
    println!("Después de pop: {:?}", pila.elementos);

    // -------- QUEUE --------
    let mut cola = Queue::new();

    cola.enqueue(Valor::Entero(1));
    cola.enqueue(Valor::Texto(String::from("mundo")));
    cola.enqueue(Valor::Decimal(2.71));
    cola.enqueue(Valor::Booleano(false));

    println!("\nQueue completa: {:?}", cola.elementos);
    println!("Frente de la cola: {:?}", cola.front());

    cola.dequeue();
    println!("Después de dequeue: {:?}", cola.elementos);
}