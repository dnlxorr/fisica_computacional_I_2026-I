import pandas as pd
import matplotlib.pyplot as plt

# Dataset estable
url = "https://raw.githubusercontent.com/Dfranzani/Bases-de-datos-para-cursos/main/2023-1/sleep2.csv"
df = pd.read_csv(url)

# Agrupar por edad (promedio)
df_group = df.groupby("Age").mean(numeric_only=True)

plt.figure()

plt.plot(df_group.index, df_group["Sleep.Duration"], marker='o', label="Horas de sueño")
plt.plot(df_group.index, df_group["Stress.Level"], marker='o', label="Estrés")

plt.title("Sueño y estrés promedio por edad")
plt.xlabel("Edad")
plt.ylabel("Valores promedio")
plt.legend()
plt.grid()

plt.show()