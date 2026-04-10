use csv::Reader;
use plotters::prelude::*;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {

    // Leer el CSV
    let mut rdr = Reader::from_path("dielectron.csv")?;

    // Guardar valores de la columna M
    let mut masses: Vec<f64> = Vec::new();

    for result in rdr.deserialize() {
        let record: std::collections::HashMap<String, String> = result?;
        if let Some(m) = record.get("M") {
            let value: f64 = m.parse()?;
            masses.push(value);
        }
    }

    // Mostrar primeros valores (equivalente a head())
    println!("Primeros valores:");
    for i in 0..5.min(masses.len()) {
        println!("{}", masses[i]);
    }

    // Definir rango del histograma
    let min = masses.iter().cloned().fold(f64::INFINITY, f64::min);
    let max = masses.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let bins = 100;
    let bin_width = (max - min) / bins as f64;

    let mut counts = vec![0u32; bins];

    for m in masses {
        let mut index = ((m - min) / bin_width) as usize;
        if index >= bins {
            index = bins - 1;
        }
        counts[index] += 1;
    }

    // Crear imagen
    let root = BitMapBackend::new("histograma.png", (800, 600)).into_drawing_area();
    root.fill(&WHITE)?;

    let y_max = *counts.iter().max().unwrap();

    let mut chart = ChartBuilder::on(&root)
        .margin(20)
        .caption("Distribution of Dielectron Invariant Mass", ("sans-serif", 30))
        .x_label_area_size(40)
        .y_label_area_size(40)
        .build_cartesian_2d(min..max, 0u32..y_max)?;

    chart.configure_mesh()
        .x_desc("Invariant Mass M")
        .y_desc("Frequency")
        .draw()?;

    chart.draw_series(
        counts.iter().enumerate().map(|(i, count)| {
            let x0 = min + i as f64 * bin_width;
            let x1 = x0 + bin_width;

            Rectangle::new([(x0, 0), (x1, *count)], BLUE.filled())
        })
    )?;

    root.present()?;

    println!("Histograma guardado como histograma.png");

    Ok(())
}