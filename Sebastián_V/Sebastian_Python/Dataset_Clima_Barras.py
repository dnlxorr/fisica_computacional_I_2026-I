import requests
import pandas as pd
import matplotlib.pyplot as plt

# API NASA
url = "https://power.larc.nasa.gov/api/temporal/daily/point"
params = {
    "parameters": "ALLSKY_SFC_SW_DWN",
    "community": "RE",
    "longitude": -75.56,
    "latitude": 6.25,
    "start": 20220101,
    "end": 20221231,
    "format": "JSON"
}

# Solicitud
response = requests.get(url, params=params)
data = response.json()

# EXTRAER BIEN LOS DATOS
df = pd.DataFrame(
    data["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"],
    index=[0]
).T

# Convertir índice a fecha
df.index = pd.to_datetime(df.index, format="%Y%m%d")

# Renombrar columna
df.columns = ["Radiacion"]

# Graficar
plt.plot(df.index, df["Radiacion"])
plt.xlabel("Fecha")
plt.ylabel("Radiación solar (kWh/m²/día)")
plt.title("Radiación solar en Medellín (2022)")
plt.show()