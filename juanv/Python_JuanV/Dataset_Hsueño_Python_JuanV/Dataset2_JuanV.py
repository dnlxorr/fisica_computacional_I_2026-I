import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

url = "https://raw.githubusercontent.com/Dfranzani/Bases-de-datos-para-cursos/main/2023-1/sleep2.csv"
df = pd.read_csv(url)

plt.figure(figsize=(10,6))

# Crear "jitter" (pequeña variación)
x = df["Sleep.Duration"] + np.random.normal(0, 0.05, size=len(df))
y = df["Stress.Level"] + np.random.normal(0, 0.05, size=len(df))

plt.scatter(x, y, s=40, alpha=0.7)

plt.title("Relación entre horas de sueño y nivel de estrés")
plt.xlabel("Horas de sueño")
plt.ylabel("Nivel de estrés")
plt.grid()

plt.show()