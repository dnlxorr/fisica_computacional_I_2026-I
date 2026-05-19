pub(crate) fn error() {
    let mut total: f64 = 0.0;

    for _ in 0..100_000 {
        total += 0.1;
    }

    println!("Resultado de sumar 0.1 cien mil veces: {}", total);
}