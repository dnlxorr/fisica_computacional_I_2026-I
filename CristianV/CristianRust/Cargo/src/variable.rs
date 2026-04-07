// main.rs
// Ejemplo de variables y estructuras de control en Rust
// Característica principal: Tipado estático, seguro y ultra eficiente en memoria

pub(crate) fn aja() {
    let gravedad: f64 = 9.81;
    let tiempo_maximo: i32 = 5;
    let experimento: &str = "Caída Libre";

    // 1. Declaramos como mutable
    let mut en_movimiento: bool = true;

    println!("--- Iniciando: {} ---", experimento);
    println!("¿Estado inicial en movimiento?: {}", en_movimiento); // <--- Úsala aquí

    for t in 0..=tiempo_maximo {
        // Rust es estricto: no mezcla enteros con decimales automáticamente.
        // Debemos convertir 't' a f64 explícitamente usando 'as f64'
        let velocidad: f64 = gravedad * (t as f64);

        // --- 3. ESTRUCTURAS DE CONTROL: CONDICIONALES ---
        // if / else if / else (Nota que en Rust no llevan paréntesis obligatorios)
        if velocidad == 0.0 {
            println!("T={}s: El objeto está en reposo.", t);
        } else if velocidad < 30.0 {
            println!("T={}s: Velocidad normal de {:.2} m/s.", t, velocidad);
        } else {
            println!("T={}s: ¡Alta velocidad! ({:.2} m/s).", t, velocidad);
        }
    }

    // 2. Cambiamos el valor
   
    en_movimiento = false;
    println!("Simulación terminada. ¿Sigue en movimiento?: {}", en_movimiento);
}