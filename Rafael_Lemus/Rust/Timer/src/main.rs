use std::time::Instant;

fn main() {
    let inicio = Instant::now();

    let suma: i32 = (1..=100).sum();

    let duracion = inicio.elapsed();

    println!("Suma: {}", suma);
    println!("Tiempo: {:?}", duracion);
}