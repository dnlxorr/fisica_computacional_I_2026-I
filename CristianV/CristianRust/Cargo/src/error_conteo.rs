pub(crate) fn errorcon() {
    let mut sumatoria_f32: f32 = 0.0;
    let mut sumatoria_f64: f64 = 0.0;
    let objetivo = 100_000;
    let incremento = 0.1;

    for _ in 0..objetivo {
        sumatoria_f32 += incremento as f32;
        sumatoria_f64 += incremento as f64;
    }

    let esperado = objetivo as f64 * incremento;

    println!("--- Sumatoria de 0.1 repetida {} veces ---", objetivo);
    println!("Resultado esperado (Matemático): {:.2}", esperado);
    println!("----------------------------------------------");

    println!("Resultado con f32 (32 bits):     {:.10}", sumatoria_f32);
    println!("Error en f32:                    {:.10}", (sumatoria_f32 as f64 - esperado).abs());

    println!("\nResultado con f64 (64 bits):     {:.10}", sumatoria_f64);
    println!("Error en f64:                    {:.10}", (sumatoria_f64 - esperado).abs());
}