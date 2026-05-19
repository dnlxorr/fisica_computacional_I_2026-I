use reqwest;
use serde_json::Value;
use chrono::{NaiveDate, Datelike};
use plotters::prelude::*;

pub(crate) fn clima() {
    // -----------------------------------
    // 1) URL y parámetros
    // -----------------------------------
    let url = "https://power.larc.nasa.gov/api/temporal/daily/point";

    let params = [
        ("parameters", "ALLSKY_SFC_SW_DWN"),
        ("community", "RE"),
        ("longitude", "-75.56"),
        ("latitude", "6.25"),
        ("start", "20220101"),
        ("end", "20220110"),
        ("format", "JSON"),
    ];

    // -----------------------------------
    // 2) Request
    // -----------------------------------
    let response = reqwest::blocking::Client::new()
        .get(url)
        .query(&params)
        .send()
        .unwrap()
        .text()
        .unwrap();

    let json: Value = serde_json::from_str(&response).unwrap();

    // -----------------------------------
    // 3) Extraer datos
    // -----------------------------------
    let datos = json["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
        .as_object()
        .unwrap();

    let mut datos_ordenados: Vec<(f64, f64)> = Vec::new();

    for (fecha_str, valor) in datos {
        let fecha = NaiveDate::parse_from_str(fecha_str, "%Y%m%d").unwrap();
        let dia = fecha.ordinal() as f64;
        let rad = valor.as_f64().unwrap();

        datos_ordenados.push((dia, rad));
    }

    // -----------------------------------
    // 4) Ordenar por día
    // -----------------------------------
    datos_ordenados.sort_by(|a, b| a.0.partial_cmp(&b.0).unwrap());

    let dias: Vec<f64> = datos_ordenados.iter().map(|(d, _)| *d).collect();
    let radiacion: Vec<f64> = datos_ordenados.iter().map(|(_, r)| *r).collect();

    // -----------------------------------
    // 5) Rangos dinámicos
    // -----------------------------------
    let x_min = dias.iter().cloned().fold(f64::INFINITY, f64::min);
    let x_max = dias.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    let y_min = radiacion.iter().cloned().fold(f64::INFINITY, f64::min);
    let y_max = radiacion.iter().cloned().fold(f64::NEG_INFINITY, f64::max);

    // -----------------------------------
    // 6) Crear gráfica
    // -----------------------------------
    let root = BitMapBackend::new("radiacion.png", (900, 600)).into_drawing_area();
    root.fill(&WHITE).unwrap();

    let mut chart = ChartBuilder::on(&root)
        .margin(20)
        .caption("Radiación solar en Medellín (2022)", ("sans-serif", 30))
        .x_label_area_size(40)
        .y_label_area_size(50)
        .build_cartesian_2d(x_min..x_max, y_min..y_max)
        .unwrap();

    // Sin cuadrícula
    chart.configure_mesh().disable_mesh().draw().unwrap();

    // -----------------------------------
    // 7) Scatter (puntos)
    // -----------------------------------
    chart.draw_series(
        dias.iter().zip(radiacion.iter()).map(|(x, y)| {
            Circle::new((*x, *y), 4, BLUE.filled())
        })
    ).unwrap();

    println!("Gráfica guardada como radiacion.png");
}