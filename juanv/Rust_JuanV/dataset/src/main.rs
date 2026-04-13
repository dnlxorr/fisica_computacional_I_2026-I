use reqwest::blocking::get;
use serde::Deserialize;
use std::collections::HashMap;
use plotters::prelude::*;

#[derive(Debug, Deserialize)]
struct Record {
    #[serde(rename = "Age")]
    age: u32,

    #[serde(rename = "Sleep.Duration")]
    sleep_duration: f64,

    #[serde(rename = "Stress.Level")]
    stress_level: f64,
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // URL del dataset
    let url = "https://raw.githubusercontent.com/Dfranzani/Bases-de-datos-para-cursos/main/2023-1/sleep2.csv";

    // Descargar CSV
    let response = get(url)?.text()?;

    // Leer CSV
    let mut rdr = csv::Reader::from_reader(response.as_bytes());

    // HashMap: edad -> (suma_sueño, suma_estres, contador)
    let mut data: HashMap<u32, (f64, f64, u32)> = HashMap::new();

    for result in rdr.deserialize() {
        let record: Record = result?;

        let entry = data.entry(record.age).or_insert((0.0, 0.0, 0));
        entry.0 += record.sleep_duration;
        entry.1 += record.stress_level;
        entry.2 += 1;
    }

    // Ordenar edades
    let mut ages: Vec<u32> = data.keys().cloned().collect();
    ages.sort();

    // Calcular promedios
    let mut avg_sleep = Vec::new();
    let mut avg_stress = Vec::new();

    for age in &ages {
        let (sum_sleep, sum_stress, count) = data[age];
        avg_sleep.push(sum_sleep / count as f64);
        avg_stress.push(sum_stress / count as f64);
    }

    // Crear imagen
    let root = BitMapBackend::new("grafica.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    let max_y = avg_sleep
        .iter()
        .chain(avg_stress.iter())
        .cloned()
        .fold(0.0, f64::max);

    let mut chart = ChartBuilder::on(&root)
        .caption("Sueño y estrés promedio por edad", ("sans-serif", 30))
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(*ages.first().unwrap()..*ages.last().unwrap(), 0f64..max_y)?;

    chart
        .configure_mesh()
        .x_desc("Edad")
        .y_desc("Valores promedio")
        .draw()?;

    // Línea sueño
    chart
        .draw_series(LineSeries::new(
            ages.iter().zip(avg_sleep.iter()).map(|(x, y)| (*x, *y)),
            &BLUE,
        ))?
        .label("Horas de sueño")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &BLUE));

    // Línea estrés
    chart
        .draw_series(LineSeries::new(
            ages.iter().zip(avg_stress.iter()).map(|(x, y)| (*x, *y)),
            &RED,
        ))?
        .label("Estrés")
        .legend(|(x, y)| PathElement::new([(x, y), (x + 20, y)], &RED));

    chart
        .configure_series_labels()
        .border_style(&BLACK)
        .draw()?;

    println!("✅ Gráfica guardada como grafica.png");

    Ok(())
}