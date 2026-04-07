use std::time::Instant;
pub(crate) fn tiempo_eje(){
    let inicio = Instant::now();

    let mut suma: u64 = 0; // Solo una vez

    for i in 1..1000 {
        suma += i;
    }

    println!("La suma total es: {}", suma); // Al usarla aquí, el warning desaparece

    let tiempo_ejecucion = inicio.elapsed();
    println!("El código tardó: {:?}", tiempo_ejecucion);
}