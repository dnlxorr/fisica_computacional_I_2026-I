use polars::prelude::*;
use plotters::prelude::*;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    // 1. Ruta del archivo
    let ruta = r"C:\Users\lezly\OneDrive - Universidad de Pamplona\Documents\computacional_I\12720.csv";

    // 2. Cargar el Dataset (Nueva sintaxis de Polars 0.41)
    let df = CsvReadOptions::default()
        .with_parse_options(
            CsvParseOptions::default()
                .with_separator(b';')
        )
        .with_has_header(true)
        .try_into_reader_with_file_path(Some(ruta.into()))?
        .finish()?;

    // 3. Filtrado de datos
    // Filtramos por Convocatoria == 'Total'
    let mask_total = df.column("Convocatoria de la prueba de acceso a la universidad")?
        .equal("Total")?;
    let df_total = df.filter(&mask_total)?;

    // Separamos "Estudiantes presentados" y "Estudiantes aprobados"
    let presentados = df_total.filter(
        &df_total.column("Concepto Educativo")?.equal("Estudiantes presentados")?
    )?;

    let aprobados = df_total.filter(
        &df_total.column("Concepto Educativo")?.equal("Estudiantes aprobados")?
    )?;

    // 4. Preparar el lienzo para las gráficas
    let root = BitMapBackend::new("analisis_rust.png", (1500, 1000)).into_drawing_area();
    root.fill(&WHITE)?;

    let root = root.titled("Análisis Comparativo: Mujeres en Acceso Universitario", ("sans-serif", 40).into_font())?;
    let areas = root.split_evenly((2, 2));

    // Función auxiliar para extraer datos como f64 para plotters
    let get_data = |df: &DataFrame, col: &str| -> Vec<f64> {
        df.column(col)
            .expect("Columna no encontrada")
            .cast(&DataType::Float64).expect("Error al convertir a float")
            .f64().expect("No es una columna f64")
            .into_no_null_iter()
            .collect()
    };

    let años = get_data(&presentados, "Periodo");
    let val_presentados = get_data(&presentados, "Total");
    let val_aprobados = get_data(&aprobados, "Total");

    // --- GRÁFICA 1: Líneas (Arriba Izquierda) ---
    {
        let mut chart = ChartBuilder::on(&areas[0])
            .caption("1. Gráfica de Líneas", ("sans-serif", 30))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(2010.0..2024.0, 0.0..100.0)?;

        chart.configure_mesh().draw()?;

        chart.draw_series(LineSeries::new(
            años.iter().zip(val_presentados.iter()).map(|(x, y)| (*x, *y)),
            &BLUE,
        ))?.label("Presentadas").legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &BLUE));

        chart.draw_series(LineSeries::new(
            años.iter().zip(val_aprobados.iter()).map(|(x, y)| (*x, *y)),
            &RED,
        ))?.label("Aprobadas").legend(|(x, y)| PathElement::new(vec![(x, y), (x + 20, y)], &RED));

        chart.configure_series_labels().border_style(&BLACK).draw()?;
    }

    // --- GRÁFICA 2: Scatter (Arriba Derecha) ---
    {
        let mut chart = ChartBuilder::on(&areas[1])
            .caption("2. Gráfica de Dispersión", ("sans-serif", 30))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(2010.0..2024.0, 0.0..100.0)?;

        chart.configure_mesh().draw()?;

        chart.draw_series(años.iter().zip(val_presentados.iter()).map(|(x, y)| Circle::new((*x, *y), 5, BLUE.filled())))?;
        chart.draw_series(años.iter().zip(val_aprobados.iter()).map(|(x, y)| Cross::new((*x, *y), 5, RED.filled())))?;
    }

    // --- GRÁFICA 3: Densidad/Alpha (Abajo Izquierda) ---
    {
        let mut chart = ChartBuilder::on(&areas[2])
            .caption("3. Gráfica de Densidad (Alpha)", ("sans-serif", 30))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(2010.0..2024.0, 0.0..100.0)?;

        chart.configure_mesh().draw()?;

        chart.draw_series(años.iter().zip(val_presentados.iter()).map(|(x, y)| Circle::new((*x, *y), 10, BLUE.mix(0.3).filled())))?;
        chart.draw_series(años.iter().zip(val_aprobados.iter()).map(|(x, y)| Circle::new((*x, *y), 10, RED.mix(0.3).filled())))?;
    }

    // --- GRÁFICA 4: Puntos (Abajo Derecha) ---
    {
        let mut chart = ChartBuilder::on(&areas[3])
            .caption("4. Gráfica de Puntos", ("sans-serif", 30))
            .margin(20)
            .x_label_area_size(40)
            .y_label_area_size(50)
            .build_cartesian_2d(2010.0..2024.0, 0.0..100.0)?;

        chart.configure_mesh().draw()?;

        chart.draw_series(años.iter().zip(val_presentados.iter()).map(|(x, y)| Circle::new((*x, *y), 2, &BLUE)))?;
        chart.draw_series(años.iter().zip(val_aprobados.iter()).map(|(x, y)| Circle::new((*x, *y), 2, &RED)))?;
    }

    root.present()?;
    println!("¡Proceso completado! Revisa el archivo 'analisis_rust.png'");

    Ok(())
}