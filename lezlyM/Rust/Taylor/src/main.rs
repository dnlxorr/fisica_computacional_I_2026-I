use ndarray::{Array1, Zip};
use plotters::prelude::*;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1. Configuración - Especificamos explícitamente f64
    let (a, b, c): (f64, f64, f64) = (1.0, -2.0, 1.0);
    let punto_a: f64 = 0.5; // Agregamos : f64 aquí

    // 2. Definición numérica
    let n = 100;
    let x_vals: Array1<f64> = Array1::linspace(-1.0, 3.0, n);

    // Función original: f(x)
    let f_original = x_vals.map(|&x| a * x.powi(2) + b * x + c);

    // 3. Expansión de Taylor (Manual)
    let f_a = a * punto_a.powi(2) + b * punto_a + c;
    let df_a = 2.0 * a * punto_a + b;
    let ddf_a = 2.0 * a;

    let taylor_manual = x_vals.map(|&x| {
        f_a + df_a * (x - punto_a) + (ddf_a / 2.0) * (x - punto_a).powi(2)
    });

    // 4. Cálculo del MSE
    let mut suma_error = 0.0;
    Zip::from(&taylor_manual).and(&f_original).for_each(|&t, &f| {
        suma_error += (t - f).powi(2);
    });
    let mse = suma_error / n as f64;
    println!("Error Cuadrático Medio (MSE): {:.1e}", mse);

    // 5. Graficación
    let root = BitMapBackend::new("taylor_plot.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .caption("Expansión de Taylor en Rust", ("sans-serif", 30))
        .margin(10)
        .x_label_area_size(30)
        .y_label_area_size(30)
        .build_cartesian_2d(-1.0..3.0, -0.5..4.0)?;

    chart.configure_mesh().draw()?;

    // Dibujar Función Original
    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(f_original.iter()).map(|(&x, &y)| (x, y)),
        &BLACK.mix(0.3),
    ))?.label("Original f(x)").legend(|(x, y)| PathElement::new(vec![(x, y), (x + 10, y)], &BLACK.mix(0.3)));

    // Dibujar Taylor Manual
    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(taylor_manual.iter()).map(|(&x, &y)| (x, y)),
        &RED,
    ))?.label("Taylor Manual").legend(|(x, y)| PathElement::new(vec![(x, y), (x + 10, y)], &RED));

    // Punto de expansión
    chart.draw_series(PointSeries::of_element(
        vec![(punto_a, f_a)],
        5,
        &GREEN,
        &|c, s, st| {
            return EmptyElement::at(c) + Circle::new((0, 0), s, st.filled());
        },
    ))?;

    chart.configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .draw()?;

    root.present()?; // Muy importante añadir esta línea para guardar el archivo
    println!("Gráfica guardada como 'taylor_plot.png'");
    Ok(())
}