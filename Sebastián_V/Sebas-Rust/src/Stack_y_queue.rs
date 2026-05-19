// =========================================
// 🔹 STACK (PILA)
// =========================================

struct Stack {
    data: Vec<String>,
}

impl Stack {
    fn new() -> Self {
        Stack { data: Vec::new() }
    }

    fn push(&mut self, item: String) {
        self.data.push(item);
    }

    fn pop(&mut self) -> Option<String> {
        self.data.pop()
    }

    fn peek(&self) -> Option<&String> {
        self.data.last()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    fn size(&self) -> usize {
        self.data.len()
    }

    fn show(&self) {
        println!("{:?}", self.data);
    }
}


// =========================================
// 🔹 QUEUE (COLA)
// =========================================

struct Queue {
    data: Vec<String>,
}

impl Queue {
    fn new() -> Self {
        Queue { data: Vec::new() }
    }

    fn enqueue(&mut self, item: String) {
        self.data.push(item);
    }

    fn dequeue(&mut self) -> Option<String> {
        if self.is_empty() {
            None
        } else {
            Some(self.data.remove(0)) // elimina el primero
        }
    }

    fn front(&self) -> Option<&String> {
        self.data.first()
    }

    fn is_empty(&self) -> bool {
        self.data.is_empty()
    }

    fn size(&self) -> usize {
        self.data.len()
    }

    fn show(&self) {
        println!("{:?}", self.data);
    }
}


// =========================================
// 🔹 PRUEBA
// =========================================

pub(crate) fn stack() {
    println!("=== STACK ===");
    let mut s = Stack::new();

    s.push("10".to_string());
    s.push("hola".to_string());
    s.push("3.14".to_string());

    s.show();

    println!("Pop: {:?}", s.pop());
    println!("Top: {:?}", s.peek());

    s.show();

    println!("\n=== QUEUE ===");
    let mut q = Queue::new();

    q.enqueue("1".to_string());
    q.enqueue("mundo".to_string());
    q.enqueue("2.5".to_string());

    q.show();

    println!("Dequeue: {:?}", q.dequeue());
    println!("Front: {:?}", q.front());

    q.show();
}