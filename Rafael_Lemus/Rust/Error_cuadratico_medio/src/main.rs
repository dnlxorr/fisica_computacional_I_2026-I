fn calcular_mse(real: &[f64], aproximado: &[f64]) -> f64 {

    if real.len() != aproximado.len() {
        panic!("Los vectores deben tener la misma longitud");
    }

    let mut suma = 0.0;

    for i in 0..real.len() {
        let diferencia = real[i] - aproximado[i];
        suma += diferencia.powi(2);
    }

    suma / real.len() as f64
}

fn main() {

    // Datos de ejemplo
    let valores_reales = vec![1.0, 2.0, 3.0, 4.0, 5.0];
    let valores_aprox = vec![0.9, 2.1, 2.9, 4.2, 4.8];

    let mse = calcular_mse(&valores_reales, &valores_aprox);

    println!("El error cuadrático medio es: {}", mse);
}