fn main() {

    // PILA (STACK)
    let mut pila = Vec::new(); // vector vacío

    // push (agregar elementos)
    pila.push(10);
    pila.push(20);
    pila.push(30);

    // pop (sacar el último)
    let sacado_pila = pila.pop();

    println!("Pila: {:?}", pila);
    println!("Sacado de pila: {:?}", sacado_pila);

    // ver el tope
    if let Some(tope) = pila.last() {
        println!("Tope actual: {:?}", tope);
    }

    //  COLA (QUEUE)
    let mut cola = Vec::new();

    // enqueue (agregar)
    cola.push(100);
    cola.push(200);
    cola.push(300);

    // dequeue (sacar el primero)
    let sacado_cola = cola.remove(0);

    println!("Cola: {:?}", cola);
    println!("Sacado de cola: {:?}", sacado_cola);

    // ver el primero
    if !cola.is_empty() {
        println!("Primero en cola: {:?}", cola[0]);
    }
}
