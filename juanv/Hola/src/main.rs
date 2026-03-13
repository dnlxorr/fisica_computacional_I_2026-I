use std::time::Instant;

fn main() {

    let inicio = Instant::now();

    let mut suma = 0;

    for i in 1..=1000 {
        suma += i;
    }

    let duracion = inicio.elapsed();

    println!("La suma de los números del 1 al 1000 es: {}", suma);
    println!("Tiempo de ejecución: {:?}", duracion);

}