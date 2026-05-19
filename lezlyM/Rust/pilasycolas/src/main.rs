use std::collections::VecDeque;

#[derive(Debug, Clone)]
struct Pedido {
    id: i32,
    producto: String,
    precio: f64,
}

fn main() {
    // Definimos los pedidos usando una estructura para mayor claridad
    let pedidos = vec![
        Pedido { id: 1, producto: String::from("Café"), precio: 2.5 },
        Pedido { id: 2, producto: String::from("Pan"), precio: 1.5 },
        Pedido { id: 3, producto: String::from("Té"), precio: 2.0 },
    ];

    // COLA: Usamos VecDeque (Double Ended Queue)
    let mut cola = VecDeque::from(pedidos.clone());

    // PILA: Un Vec estándar funciona perfectamente como pila
    let mut pila = pedidos.clone();

    println!("--- 🛒 PROCESANDO VENTAS ---");

    // COLA (FIFO): pop_front() equivale a popleft() de Python
    if let Some(cliente_f) = cola.pop_front() {
        println!(
            "COLA (Primero): Atendiendo pedido {} de {}",
            cliente_f.id, cliente_f.producto
        );
    }

    // PILA (LIFO): pop() funciona igual que en Python
    if let Some(cliente_p) = pila.pop() {
        println!(
            "PILA (Último): Atendiendo pedido {} de {}",
            cliente_p.id, cliente_p.producto
        );
    }
}