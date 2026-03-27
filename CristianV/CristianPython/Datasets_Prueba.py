import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. DEFINIR LA URL DIRECTA AL ARCHIVO CSV
# ==========================================
# Este es un dataset de ejemplo de la NOAA con datos diarios.
# Contiene columnas como DATE (Fecha), TMAX (Temp Máxima), TMIN (Temp Mínima), PRCP (Precipitación).
url_clima_historico = 'https://raw.githubusercontent.com/vega/vega/master/docs/data/seattle-weather.csv'

print("Cargando datos desde la web... por favor espere.")

try:
    # ==========================================
    # 2. LEER LOS DATOS DIRECTAMENTE A PANDAS
    # ==========================================
    # pandas detecta que es una URL y descarga el contenido en memoria.
    df = pd.read_csv(url_clima_historico)

    # ==========================================
    # 3. PREPROCESAMIENTO (Esencial en Física)
    # ==========================================
    # Convertir la columna 'date' de texto a formato Fecha (Datetime)
    df['date'] = pd.to_datetime(df['date'])

    # Establecer la fecha como el índice del DataFrame (facilita graficar series temporales)
    df.set_index('date', inplace=True)

    # Mostrar las primeras filas y estructura para verificar
    print("\n--- Estructura del Dataset ---")
    print(df.info())
    print("\n--- Primeras 5 filas ---")
    print(df.head())

    # ==========================================
    # 4. GRAFICAR LOS DATOS
    # ==========================================
    print("\nGenerando gráfico...")

    # Crear una figura con dos subgráficos (uno para temperatura, otro para lluvia)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

    # Gráfico 1: Temperaturas Máxima y Mínima
    ax1.plot(df.index, df['temp_max'], label='Temp Máxima (°C)', color='red', alpha=0.7)
    ax1.plot(df.index, df['temp_min'], label='Temp Mínima (°C)', color='blue', alpha=0.7)
    ax1.fill_between(df.index, df['temp_min'], df['temp_max'], color='gray', alpha=0.2)  # Relleno entre ambas
    ax1.set_title('Temperaturas Diarias Históricas')
    ax1.set_ylabel('Temperatura (°C)')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.5)

    # Gráfico 2: Precipitación
    ax2.bar(df.index, df['precipitation'], label='Precipitación (mm)', color='green', alpha=0.8)
    ax2.set_title('Precipitación Diaria')
    ax2.set_ylabel('Lluvia (mm)')
    ax2.set_xlabel('Fecha')
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    # Ajustar diseño y mostrar
    plt.tight_layout()
    print("Gráfico generado exitosamente.")
    plt.show()

except Exception as e:
    print(f"Ocurrió un error al intentar cargar o graficar los datos: {e}")