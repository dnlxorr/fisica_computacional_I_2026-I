

use std::time::Instant;

fn main() {
    // 1. Guardar el tiempo de inicio
    let inicio = Instant::now();


    let mut suma: u64 = 0;
    for i in 1..=1_000 {
        suma += i;
    }
    // -------------------------

    // 2. Calcular la duración (elapsed calcula la diferencia automáticamente)
    let tiempo_ejecucion = inicio.elapsed();

    // 3. Imprimir el resultado
    // Usamos {:?} para que Rust elija automáticamente la mejor unidad (ej: 1.2ms, 5µs)
    println!("El código tardó: {:?}", tiempo_ejecucion);

    // Si prefieres forzar el formato a segundos con 4 decimales:
    println!("En segundos exactos: {:.4} s", tiempo_ejecucion.as_secs_f64());
}