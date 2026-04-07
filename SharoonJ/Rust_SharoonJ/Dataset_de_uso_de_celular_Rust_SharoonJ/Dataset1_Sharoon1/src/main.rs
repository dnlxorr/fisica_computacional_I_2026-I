use csv::ReaderBuilder;
use plotters::prelude::*;
use serde::Deserialize;
use std::collections::HashMap;

#[derive(Debug, Deserialize)]
struct Record {
    #[serde(rename = "Age")]
    age: u32,

    #[serde(rename = "App_Usage_Time")]
    app_usage_time: f64,

    #[serde(rename = "Screen_On_Time")]
    screen_on_time: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = "https://raw.githubusercontent.com/Mikhthad/Mobile-Device-Usage-and-User-Behavior-Dataset/main/user_behavior_dataset.csv";

    // Descargar datos
    let data = reqwest::blocking::get(url)?.text()?;

    let mut rdr = ReaderBuilder::new().from_reader(data.as_bytes());

    let mut grouped: HashMap<u32, (f64, f64, u32)> = HashMap::new();

    // Agrupar por edad
    for result in rdr.deserialize() {
        let record: Record = result?;

        let entry = grouped.entry(record.age).or_insert((0.0, 0.0, 0));
        entry.0 += record.app_usage_time;
        entry.1 += record.screen_on_time;
        entry.2 += 1;
    }

    // Calcular promedios
    let mut ages: Vec<u32> = grouped.keys().cloned().collect();
    ages.sort();

    let mut app_avg = Vec::new();
    let mut screen_avg = Vec::new();

    for age in &ages {
        let (app_sum, screen_sum, count) = grouped[age];
        app_avg.push(app_sum / count as f64);
        screen_avg.push(screen_sum / count as f64);
    }

    // Crear gráfico
    let root = BitMapBackend::new("grafica.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    let mut chart = ChartBuilder::on(&root)
        .caption("Uso promedio del celular por edad", ("sans-serif", 30))
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(
            *ages.first().unwrap()..*ages.last().unwrap(),
            0f64..100f64,
        )?;

    chart.configure_mesh()
        .x_desc("Edad")
        .y_desc("Tiempo (0 a 100)")
        .draw()?;

    // Línea uso apps
    chart.draw_series(LineSeries::new(
        ages.iter().zip(app_avg.iter()).map(|(x, y)| (*x, *y)),
        &BLUE,
    ))?
        .label("Uso de apps")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &BLUE));

    // Línea pantalla
    chart.draw_series(LineSeries::new(
        ages.iter().zip(screen_avg.iter()).map(|(x, y)| (*x, *y)),
        &RED,
    ))?
        .label("Pantalla")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &RED));

    chart.configure_series_labels().draw()?;

    println!("Gráfica guardada como grafica.png");

    Ok(())
}