use plotters::prelude::*;

fn taylor_4(x: f64) -> f64 {
    x.exp()
        + (3.0 * x).exp() / 6.0
        + (5.0 * x).exp() / 120.0
        + (7.0 * x).exp() / 5040.0
}

fn taylor_7(x: f64) -> f64 {
    x.exp()
        + (3.0 * x).exp() / 6.0
        + (5.0 * x).exp() / 120.0
        + (7.0 * x).exp() / 5040.0
        + (9.0 * x).exp() / 362880.0
        + (11.0 * x).exp() / 39916800.0
        + (13.0 * x).exp() / 6227020800.0
}

pub(crate) fn aprox() {
    let n = 500;
    let x_min = -2.0;
    let x_max = 2.0;

    let mut x_vals = Vec::new();
    let mut y4_vals = Vec::new();
    let mut y7_vals = Vec::new();

    // -----------------------------------
    // 1) Generar datos
    // -----------------------------------
    for i in 0..n {
        let x = x_min + (x_max - x_min) * (i as f64) / (n as f64);
        x_vals.push(x);
        y4_vals.push(taylor_4(x));
        y7_vals.push(taylor_7(x));
    }

    // -----------------------------------
    // 2) Calcular MSE
    // -----------------------------------
    let mut mse = 0.0;
    for i in 0..n {
        let diff = y4_vals[i] - y7_vals[i];
        mse += diff * diff;
    }
    mse /= n as f64;

    println!("MSE = {}", mse);

    // -----------------------------------
    // 3) Encontrar rango dinámico en Y
    // -----------------------------------
    let mut y_min = f64::INFINITY;
    let mut y_max = f64::NEG_INFINITY;

    for i in 0..n {
        y_min = y_min.min(y4_vals[i]).min(y7_vals[i]);
        y_max = y_max.max(y4_vals[i]).max(y7_vals[i]);
    }

    // Margen extra para que no quede pegado
    let margen = (y_max - y_min) * 0.1;
    y_min -= margen;
    y_max += margen;

    // -----------------------------------
    // 4) Crear gráfica
    // -----------------------------------
    let root = BitMapBackend::new("grafica.png", (1000, 600)).into_drawing_area();
    root.fill(&WHITE).unwrap();

    let mut chart = ChartBuilder::on(&root)
        .margin(20)
        .caption("Aproximación de Taylor de sinh(e^x)", ("sans-serif", 30))
        .x_label_area_size(40)
        .y_label_area_size(50)
        .build_cartesian_2d(x_min..x_max, y_min..y_max)
        .unwrap();

    // SIN cuadrícula (más limpio)
    chart
        .configure_mesh()
        .disable_mesh()
        .draw()
        .unwrap();

    // -----------------------------------
    // 5) Dibujar curvas
    // -----------------------------------
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().zip(y7_vals.iter()).map(|(x, y)| (*x, *y)),
            &BLUE,
        ))
        .unwrap()
        .label("Taylor 7 términos")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));

    chart
        .draw_series(LineSeries::new(
            x_vals.iter().zip(y4_vals.iter()).map(|(x, y)| (*x, *y)),
            &RED,
        ))
        .unwrap()
        .label("Taylor 4 términos")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    // Leyenda
    chart
        .configure_series_labels()
        .border_style(&BLACK)
        .draw()
        .unwrap();

    // -----------------------------------
    // 6) Mostrar MSE
    // -----------------------------------
    root.draw(&Text::new(
        format!("MSE = {:.2e}", mse),
        (80, 50),
        ("sans-serif", 20).into_font(),
    ))
        .unwrap();
}