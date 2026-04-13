use std::time::Instant;

fn main() {
    let inicio = Instant::now();

    let mut suma = 0;

    for i in 1..=1000 {
        suma += i;
        println!("Suma hasta {} = {}", i, suma);
    }

    let duracion = inicio.elapsed();

    println!("--------------------------------");
    println!("La suma total es: {}", suma);
    println!("Tiempo de ejecución: {:?}", duracion);
}