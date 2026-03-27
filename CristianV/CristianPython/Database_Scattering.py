import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. OBTENCIÓN Y PREPARACIÓN DE DATOS
# ==========================================
# Usamos el mismo link directo (Raw CSV)
url_clima_historico = 'https://raw.githubusercontent.com/vega/vega/master/docs/data/seattle-weather.csv'

print("Cargando datos desde Seattle...")

try:
    df = pd.read_csv(url_clima_historico)

    # Preprocesamiento esencial: Fechas
    df['date'] = pd.to_datetime(df['date'])
    # NOTA: No estableceremos la fecha como índice esta vez,
    # la pasaremos explícitamente en el Eje X del scatter.

    # print(df.head()) # Opcional: Descomenta para ver la estructura

    # ==========================================
    # 2. CREACIÓN DEL GRÁFICO (SCATTER PLOT)
    # ==========================================
    print("Generando scatter plot correlacionado...")

    # Creamos un lienzo de un solo gráfico grande
    fig, ax = plt.subplots(figsize=(14, 8))

    # --- El comando clave: scatter ---
    # x: Fechas
    # y: Temp Max
    # s (size): Precipitación (multiplicada por 10 para que sea visible)
    # c (color): Temp Max (asociada al gradiente)
    # cmap: 'coolwarm' (Azul=Frío, Rojo=Calor)
    scatter = ax.scatter(df['date'], df['temp_max'],
                         s=df['precipitation'] * 10,  # Escalamos el tamaño
                         c=df['temp_max'],  # Asociamos color a temperatura
                         cmap='coolwarm',  # Gradiente intuitivo
                         alpha=0.6,  # Transparencia para ver puntos superpuestos
                         edgecolors='none')  # Sin bordes para un look más limpio

    # ==========================================
    # 3. EXPLICACIÓN DEL COLOR (COLORBAR)
    # ==========================================
    # Añadimos una barra lateral que explica qué significan los colores
    cbar = plt.colorbar(scatter)
    cbar.set_label('Temperatura Máxima (°C)', fontsize=12)

    # ==========================================
    # 4. TÍTULOS Y ETIQUETAS
    # ==========================================
    ax.set_title('Clima Diario de Seattle (2012-2015)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Temperatura Máxima (°C)', fontsize=13)
    ax.set_xlabel('Año', fontsize=13)

    # Añadimos una cuadrícula tenue para facilitar la lectura
    ax.grid(True, linestyle='--', alpha=0.3)

    # Explicación del Tamaño (Añadido manualmente al título o como texto)
    ax.text(0.5, -0.12, '* El TAMAÑO de los puntos representa la cantidad de Precipitación (mm)',
            transform=ax.transAxes, ha='center', fontsize=10, style='italic')

    # Ajustamos para que no se corten los textos
    plt.tight_layout()
    print("Gráfico generado. Mostrando...")
    plt.show()

except Exception as e:
    print(f"Ocurrió un error: {e}")