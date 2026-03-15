use std::time::Instant;

fn main() {
    // Tiempo inicial
    let inicio = Instant::now();

    // Programa: suma de 1 hasta 100000
    let mut suma: u64 = 0;

    for i in 1..=100000 {
        suma += i;
    }

    // Tiempo final
    let duracion = inicio.elapsed();

    println!("Resultado de la suma: {}", suma);
    println!("Tiempo de ejecución: {:?}", duracion);
}