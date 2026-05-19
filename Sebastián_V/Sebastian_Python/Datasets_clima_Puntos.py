import requests
import pandas as pd
import matplotlib.pyplot as plt

# API NASA POWER
url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",
    "community": "RE",
    "longitude": -75.56,
    "latitude": 6.25,
    "start": 20220101,
    "end": 20220110,
    "format": "JSON"
}

# Solicitud
response = requests.get(url, params=params)
data = response.json()

# Extraer datos correctamente
df = pd.DataFrame(
    data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"],
    index=[0]
).T

# Convertir fechas
df.index = pd.to_datetime(df.index, format="%Y%m%d")

# Renombrar columna
df.columns = ["Radiacion"]

# Crear variable: día del año
df["dia"] = df.index.dayofyear

# Gráfica SOLO puntos
plt.scatter(df["dia"], df["Radiacion"])

# Etiquetas
plt.xlabel("Día del año")
plt.ylabel("Radiación solar (kWh/m²/día)")
plt.title("Radiación solar en Medellín (2022)")

# Mostrar
plt.show()