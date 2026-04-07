use plotters::prelude::*;
use std::f64::consts::E;

fn main() {

    // Valores de x
    let mut x_vals: Vec<f64> = Vec::new();
    let mut y_vals: Vec<f64> = Vec::new();
    let mut t3_vals: Vec<f64> = Vec::new();
    let mut t6_vals: Vec<f64> = Vec::new();

    let n = 100;
    let start = -2.0;
    let end = 2.0;

    for i in 0..n {
        let x = start + (end - start) * (i as f64) / (n as f64);
        x_vals.push(x);

        // Función real
        let y = E.powf(x);
        y_vals.push(y);

        // Taylor 3 términos
        let t3 = 1.0 + x + (x.powi(2)) / 2.0;
        t3_vals.push(t3);

        // Taylor 6 términos
        let t6 = 1.0
            + x
            + (x.powi(2)) / 2.0
            + (x.powi(3)) / 6.0
            + (x.powi(4)) / 24.0
            + (x.powi(5)) / 120.0;
        t6_vals.push(t6);
    }

    // -------- GRÁFICA --------
    let root = BitMapBackend::new("grafica.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE).unwrap();

    let mut chart = ChartBuilder::on(&root)
        .caption("Aproximación de e^x con Series de Taylor", ("sans-serif", 20))
        .margin(20)
        .x_label_area_size(30)
        .y_label_area_size(40)
        .build_cartesian_2d(-2.0..2.0, 0.0..8.0)
        .unwrap();

    chart.configure_mesh().draw().unwrap();

    // Función real
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().zip(y_vals.iter()).map(|(x, y)| (*x, *y)),
            &BLUE,
        ))
        .unwrap()
        .label("e^x (real)")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &BLUE));

    // Taylor 3
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().zip(t3_vals.iter()).map(|(x, y)| (*x, *y)),
            &RED,
        ))
        .unwrap()
        .label("Taylor 3 términos")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &RED));

    // Taylor 6
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().zip(t6_vals.iter()).map(|(x, y)| (*x, *y)),
            &GREEN,
        ))
        .unwrap()
        .label("Taylor 6 términos")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &GREEN));

    chart.configure_series_labels().draw().unwrap();

    println!("Gráfica guardada como grafica.png");

    // -------- ERROR CUADRÁTICO MEDIO --------
    let mut ecm_t3 = 0.0;
    let mut ecm_t6 = 0.0;

    for i in 0..n {
        ecm_t3 += (y_vals[i] - t3_vals[i]).powi(2);
        ecm_t6 += (y_vals[i] - t6_vals[i]).powi(2);
    }

    ecm_t3 /= n as f64;
    ecm_t6 /= n as f64;

    println!("ECM (3 términos): {}", ecm_t3);
    println!("ECM (6 términos): {}", ecm_t6);
}