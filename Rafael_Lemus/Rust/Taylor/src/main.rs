use plotters::prelude::*;

fn factorial(n: u64) -> f64 {
    (1..=n).fold(1.0, |acc, x| acc * x as f64)
}

fn f(x: f64) -> f64 {
    x.sin()
}

fn taylor3(x: f64) -> f64 {
    x - x.powi(3) / factorial(3) + x.powi(5) / factorial(5)
}

fn taylor6(x: f64) -> f64 {
    x
        - x.powi(3) / factorial(3)
        + x.powi(5) / factorial(5)
        - x.powi(7) / factorial(7)
        + x.powi(9) / factorial(9)
        - x.powi(11) / factorial(11)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {

    let n = 200;
    let start = -3.0;
    let end = 3.0;

    let step = (end - start) / (n as f64 - 1.0);

    let mut x_vals = Vec::new();
    let mut f_vals = Vec::new();
    let mut t3_vals = Vec::new();
    let mut t6_vals = Vec::new();

    for i in 0..n {
        let x = start + i as f64 * step;

        x_vals.push(x);
        f_vals.push(f(x));
        t3_vals.push(taylor3(x));
        t6_vals.push(taylor6(x));
    }

    let root = BitMapBackend::new("taylor.png", (800,600)).into_drawing_area();
    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .margin(20)
        .caption("Serie de Taylor", ("sans-serif", 30))
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(-3.0..3.0, -2.0..2.0)?;

    chart.configure_mesh()
        .x_desc("x")
        .y_desc("y")
        .draw()?;

    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(f_vals.iter()).map(|(x,y)| (*x,*y)),
        &BLUE
    ))?.label("sin(x)");

    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(t3_vals.iter()).map(|(x,y)| (*x,*y)),
        &RED
    ))?.label("Taylor 3");

    chart.draw_series(LineSeries::new(
        x_vals.iter().zip(t6_vals.iter()).map(|(x,y)| (*x,*y)),
        &GREEN
    ))?.label("Taylor 6");

    chart.configure_series_labels().border_style(&BLACK).draw()?;

    root.present()?;

    println!("Gráfica guardada como taylor.png");

    Ok(())
}