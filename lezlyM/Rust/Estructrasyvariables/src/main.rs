fn main() {
    // Variables básicas (Rust infiere los tipos, pero son estáticos)
    let nombre_tienda = "Coffee";
    let abierto = true;
    let precio_base = 2.50;
    // capacidad_maxima no se usa en el script original, pero aquí está:
    // let capacidad_maxima = 50;

    // Vectores para las listas y HashMap para los diccionarios
    let menu = vec!["Espresso", "Latte", "Capuchino"];

    // Necesitamos importar HashMap para usar diccionarios
    use std::collections::HashMap;
    let mut stock = HashMap::new();
    stock.insert("granos", 10);
    stock.insert("leche", 5);
    stock.insert("vasos", 100);

    println!("--- Bienvenidos a {} ---", nombre_tienda);

    // Verificación de condiciones
    // Usamos .get().unwrap_or() para acceder a valores del mapa de forma segura
    if abierto && *stock.get("granos").unwrap_or(&0) > 0 {
        println!("Estado: Estamos listos para atenderte.");

        println!("\nNuestro menú de hoy:");

        // El método .iter().enumerate() equivale al enumerate() de Python
        for (i, cafe) in menu.iter().enumerate() {
            let indice = i + 1; // En Rust los índices empiezan en 0
            let precio_actual = precio_base + (indice as f64);
            println!("{}. {} - ${:.2}", indice, cafe, precio_actual);
        }
    } else {
        println!("Estado: Lo sentimos, estamos cerrados o sin suministros.");
    }

    // Bucle While
    let mut clientes_esperando = 3;
    println!("\nAtendiendo fila...");

    while clientes_esperando > 0 {
        println!("Sirviendo café... Quedan {} personas.", clientes_esperando);
        clientes_esperando -= 1; // Rust no tiene clientes_esperando--
    }

    println!("¡Fila terminada!");
}