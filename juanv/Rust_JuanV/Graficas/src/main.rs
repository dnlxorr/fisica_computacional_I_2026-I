use plotters::prelude::*;
use std::f64::consts::PI;

// Función original
fn f(x: f64) -> f64 {
    x.sin()
}

// Factorial
fn factorial(n: u32) -> f64 {
    (1..=n).fold(1.0, |acc, i| acc * i as f64)
}

// Taylor 3 términos
fn taylor_3(x: f64) -> f64 {
    x - x.powi(3) / factorial(3) + x.powi(5) / factorial(5)
}

// Taylor 6 términos
fn taylor_6(x: f64) -> f64 {
    x
        - x.powi(3) / factorial(3)
        + x.powi(5) / factorial(5)
        - x.powi(7) / factorial(7)
        + x.powi(9) / factorial(9)
        - x.powi(11) / factorial(11)
}

// Error cuadrático medio
fn mse(real: &[f64], aprox: &[f64]) -> f64 {
    real.iter()
        .zip(aprox.iter())
        .map(|(r, a)| (r - a).powi(2))
        .sum::<f64>()
        / real.len() as f64
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Rango de valores
    let x_vals: Vec<f64> = (0..100)
        .map(|i| -3.0 + 6.0 * i as f64 / 99.0)
        .collect();

    // Evaluaciones
    let y_real: Vec<f64> = x_vals.iter().map(|&x| f(x)).collect();
    let y_t3: Vec<f64> = x_vals.iter().map(|&x| taylor_3(x)).collect();
    let y_t6: Vec<f64> = x_vals.iter().map(|&x| taylor_6(x)).collect();

    // Errores
    let error_t3 = mse(&y_real, &y_t3);
    let error_t6 = mse(&y_real, &y_t6);

    println!("Error cuadrático medio (3 términos): {}", error_t3);
    println!("Error cuadrático medio (6 términos): {}", error_t6);

    // Crear imagen
    let root = BitMapBackend::new("taylor_sin.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    // Crear gráfico
    let mut chart = ChartBuilder::on(&root)
        .caption("Aproximación de sin(x) con Taylor", ("sans-serif", 30))
        .margin(20)
        .x_label_area_size(30)
        .y_label_area_size(30)
        .build_cartesian_2d(-3.0..3.0, -2.0..2.0)?;

    chart.configure_mesh().draw()?;

    // Función real
    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(y_real.iter()).map(|(&x, &y)| (x, y)),
        &BLUE,
    ))?;

    // Taylor 3
    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(y_t3.iter()).map(|(&x, &y)| (x, y)),
        &RED,
    ))?;

    // Taylor 6
    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(y_t6.iter()).map(|(&x, &y)| (x, y)),
        &GREEN,
    ))?;

    root.present()?;

    println!("Gráfica guardada como taylor_sin.png");

    Ok(())
}