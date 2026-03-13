fn main() {
    println!("Hello, World!");
}
use std::time::Instant;

fn main() {
    // 1. Iniciamos el cronómetro de alta precisión
    let inicio = Instant::now();

    // 2. Ejecutamos la acción
    println!("Hello, World!");

    // 3. Calculamos el tiempo transcurrido
    let duracion = inicio.elapsed();

    println!("\n--- Estadísticas de Rust ---");
    // Mostramos el tiempo en microsegundos o nanosegundos
    // porque Rust es extremadamente rápido para un simple print.
    println!("Tiempo total: {:?}", duracion);
    println!("En nanosegundos: {} ns", duracion.as_nanos());
}