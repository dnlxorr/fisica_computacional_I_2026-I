use plotters::prelude::*;

// Función auxiliar para calcular el factorial y devolverlo como f64
fn factorial(n: u64) -> f64 {
    (1..=n).product::<u64>() as f64
}

// Función original (seno)
fn fun_org(x: f64) -> f64 {
    x.sin()
}

// Función de aproximación por Taylor con 3 términos
fn fun_aprox1(x: f64) -> f64 {
    x - (x.powi(3) / factorial(3)) + (x.powi(5) / factorial(5))
}

// Función de aproximación por Taylor con 6 términos
fn fun_aprox2(x: f64) -> f64 {
    x - (x.powi(3) / factorial(3)) + (x.powi(5) / factorial(5))
        - (x.powi(7) / factorial(7)) + (x.powi(9) / factorial(9))
        - (x.powi(11) / factorial(11))
}

// Función para calcular el Error Cuadrático Medio (ECM) de Aprox1
fn ecm1(x_vals: &[f64]) -> f64 {
    let sum_sq_err: f64 = x_vals
        .iter()
        .map(|&x| (fun_org(x) - fun_aprox1(x)).powi(2))
        .sum();
    sum_sq_err / x_vals.len() as f64
}

// Función para calcular el Error Cuadrático Medio (ECM) de Aprox2
fn ecm2(x_vals: &[f64]) -> f64 {
    let sum_sq_err: f64 = x_vals
        .iter()
        .map(|&x| (fun_org(x) - fun_aprox2(x)).powi(2))
        .sum();
    sum_sq_err / x_vals.len() as f64
}

pub(crate) fn aprox() -> Result<(), Box<dyn std::error::Error>> {
    // Equivalente a np.linspace(-3, 3, 500)
    let n_points = 500;
    let x_vals: Vec<f64> = (0..n_points)
        .map(|i| -3.0 + (6.0 * i as f64) / (n_points - 1) as f64)
        .collect();

    // Calcular los ECM
    let ecm1_val = ecm1(&x_vals);
    let ecm2_val = ecm2(&x_vals);

    // Imprimir los valores en consola
    println!("ECM1: {:.5}", ecm1_val);
    println!("ECM2: {:.5}", ecm2_val);

    // Configuración del área de dibujo (Backend)
    let root_area = BitMapBackend::new("grafico_taylor.png", (800, 600)).into_drawing_area();
    root_area.fill(&WHITE)?;

    let title = format!(
        "Grafico de Taylor de x\nECM Orden 3: {:.5} | ECM Orden 6: {:.5}",
        ecm1_val, ecm2_val
    );

    // Construcción de la gráfica
    let mut chart = ChartBuilder::on(&root_area)
        .caption(title, ("sans-serif", 20).into_font())
        .margin(10)
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(-3.0_f64..3.0_f64, -1.5_f64..1.5_f64)?;

    // Equivalente a plt.grid(True) y plt.xlabel / plt.ylabel
    chart
        .configure_mesh()
        .x_desc("x")
        .y_desc("y")
        .draw()?;

    // Plot: Función Original (Línea más gruesa para emular linewidth=3)
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().map(|&x| (x, fun_org(x))),
            ShapeStyle::from(&BLACK).stroke_width(3),
        ))?
        .label("Org")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], ShapeStyle::from(&BLACK).stroke_width(3)));

    // Plot: Aprox1
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().map(|&x| (x, fun_aprox1(x))),
            &BLUE,
        ))?
        .label("Aprox1")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));

    // Plot: Aprox2
    chart
        .draw_series(LineSeries::new(
            x_vals.iter().map(|&x| (x, fun_aprox2(x))),
            &RED,
        ))?
        .label("Aprox2")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    // Equivalente a plt.legend()
    chart
        .configure_series_labels()
        .background_style(&WHITE.mix(0.8))
        .border_style(&BLACK)
        .position(SeriesLabelPosition::UpperLeft)
        .draw()?;

    // Asegurarse de que el archivo de imagen se guarde
    root_area.present()?;
    println!("Gráfica guardada exitosamente como 'grafico_taylor.png'");

    Ok(())
}