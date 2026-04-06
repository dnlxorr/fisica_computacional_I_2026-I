
use chrono::NaiveDate;
use plotters::prelude::*;
use polars::prelude::*;
use reqwest::blocking::get;
use std::io::Cursor;

pub(crate) fn clima() -> Result<(), Box<dyn std::error::Error>> {
    // ==========================================
    // 1. DEFINIR LA URL DIRECTA AL ARCHIVO CSV
    // ==========================================
    let url = "https://raw.githubusercontent.com/vega/vega/master/docs/data/seattle-weather.csv";
    println!("Cargando datos desde la web... por favor espere.");

    // Descargar el contenido como texto en memoria
    let response_text = get(url)?.text()?;
    let cursor = Cursor::new(response_text);

    // ==========================================
    // 2 y 3. LEER LOS DATOS Y PREPROCESAR (Polars)
    // ==========================================
    // Cargamos el CSV en un DataFrame de Polars
    let df = CsvReadOptions::default()
        .with_has_header(true)
        .into_reader_with_file_handle(cursor)
        .finish()?;

    println!("\n--- Estructura del Dataset ---");
    println!("{:?}", df.schema());
    println!("\n--- Primeras 5 filas ---");
    println!("{:?}", df.head(Some(5)));

    // Extraer las columnas como vectores de Rust para poder graficarlas
    let date_series = df.column("date")?.str()?;
    let temp_max_series = df.column("temp_max")?.f64()?;
    let temp_min_series = df.column("temp_min")?.f64()?;
    let precip_series = df.column("precipitation")?.f64()?;

    // Parsear las fechas y limpiar valores nulos
    let dates: Vec<NaiveDate> = date_series
        .into_iter()
        .filter_map(|s| s.map(|val| NaiveDate::parse_from_str(val, "%Y-%m-%d").unwrap()))
        .collect();

    let temp_max: Vec<f64> = temp_max_series.into_iter().flatten().collect();
    let temp_min: Vec<f64> = temp_min_series.into_iter().flatten().collect();
    let precip: Vec<f64> = precip_series.into_iter().flatten().collect();

    if dates.is_empty() {
        return Err("No se encontraron datos válidos".into());
    }

    // ==========================================
    // 4. GRAFICAR LOS DATOS (Plotters)
    // ==========================================
    println!("\nGenerando gráfico en 'clima_historico.png'...");

    // Crear el lienzo de dibujo (1200x1000 píxeles)
    let root = BitMapBackend::new("clima_historico.png", (1200, 1000)).into_drawing_area();
    root.fill(&WHITE)?;

    // Dividir la imagen en dos subgráficos (70% superior para temperatura, 30% inferior para precipitación)
    let (upper, lower) = root.split_vertically(700);

    // Rango de fechas para el eje X
    let x_range = dates[0]..dates[dates.len() - 1];

    // --- GRÁFICO 1: Temperaturas ---
    let mut chart_temp = ChartBuilder::on(&upper)
        .caption("Temperaturas Diarias Históricas", ("sans-serif", 30).into_font())
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(50)
        .build_cartesian_2d(x_range.clone(), -10.0f64..45.0f64)?; // Rango aprox de Temp en Y

    chart_temp.configure_mesh()
        .y_desc("Temperatura (°C)")
        .draw()?;

    // Línea de Temp Máxima
    chart_temp.draw_series(LineSeries::new(
        dates.iter().zip(temp_max.iter()).map(|(x, y)| (*x, *y)),
        &RED,
    ))?
        .label("Temp Máxima (°C)")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

    // Línea de Temp Mínima
    chart_temp.draw_series(LineSeries::new(
        dates.iter().zip(temp_min.iter()).map(|(x, y)| (*x, *y)),
        &BLUE,
    ))?
        .label("Temp Mínima (°C)")
        .legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));

    chart_temp.configure_series_labels().background_style(&WHITE).border_style(&BLACK).draw()?;

    // --- GRÁFICO 2: Precipitación ---
    let mut chart_precip = ChartBuilder::on(&lower)
        .caption("Precipitación Diaria", ("sans-serif", 30).into_font())
        .margin(20)
        .x_label_area_size(40)
        .y_label_area_size(50)
        .build_cartesian_2d(x_range, 0.0f64..65.0f64)?; // Rango aprox de Lluvia en Y

    chart_precip.configure_mesh()
        .x_desc("Fecha")
        .y_desc("Lluvia (mm)")
        .draw()?;

    // Dibujar barras de precipitación
    chart_precip.draw_series(
        dates.iter().zip(precip.iter()).map(|(x, y)| {
            // Se dibuja un rectángulo estrecho como "barra" para cada día
            let p0 = (*x, 0.0);
            let p1 = (*x, *y);
            PathElement::new(vec![p0, p1], GREEN.stroke_width(2))
        }),
    )?;

    // Asegurar que el archivo se guarde correctamente
    root.present()?;
    println!("Gráfico generado exitosamente. Revisa el archivo 'clima_historico.png' en tu carpeta raíz.");

    Ok(())
}