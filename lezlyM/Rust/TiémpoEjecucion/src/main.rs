use std::collections::HashMap;
use std::time::Instant;

fn main() {
    // Iniciamos el cronómetro
    let inicio = Instant::now();

    let nombre_tienda = "Rust Coffee";
    let abierto = true;
    let precio_base = 2.50;
    // let capacidad_maxima = 50; // No se usa en el script, pero se puede declarar

    let menu = vec!["Espresso", "Latte", "Capuchino"];

    // Usamos HashMap para el stock
    let mut stock = HashMap::new();
    stock.insert("granos", 10);
    stock.insert("leche", 5);
    stock.insert("vasos", 100);

    println!("--- Bienvenidos a {} ---", nombre_tienda);

    // Verificación de condiciones
    // .get() devuelve una referencia opcional, usamos * para de-referenciar
    if abierto && *stock.get("granos").unwrap_or(&0) > 0 {
        println!("Estado: Estamos listos para atenderte.");
        println!("\nNuestro menú de hoy:");

        for (i, cafe) in menu.iter().enumerate() {
            let indice = i + 1;
            let precio_actual = precio_base + (indice as f64);
            // :.2 para mostrar dos decimales en el precio
            println!("{}. {} - ${:.2}", indice, cafe, precio_actual);
        }
    } else {
        println!("Estado: Lo sentimos, estamos cerrados o sin suministros.");
    }

    let mut clientes_esperando = 3;
    println!("\nAtendiendo fila...");

    while clientes_esperando > 0 {
        println!("Sirviendo café... Quedan {} personas.", clientes_esperando);
        clientes_esperando -= 1;
    }

    // Calculamos el tiempo transcurrido
    let duracion = inicio.elapsed();

    println!("\n{}", "=".repeat(30));
    println!("¡Fila terminada!");
    // .as_secs_f64() nos da el tiempo en segundos con precisión decimal
    println!("Tiempo de ejecución: {:.6?} segundos", duracion.as_secs_f64());
    println!("{}", "=".repeat(30));
}