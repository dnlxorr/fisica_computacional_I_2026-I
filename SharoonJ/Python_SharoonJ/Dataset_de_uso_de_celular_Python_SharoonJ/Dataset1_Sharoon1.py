import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/Mikhthad/Mobile-Device-Usage-and-User-Behavior-Dataset/main/user_behavior_dataset.csv"
df = pd.read_csv(url)

# Agrupar por edad (promedio)
df_group = df.groupby("Age").mean(numeric_only=True)

plt.figure()
plt.plot(df_group.index, df_group["App_Usage_Time"], marker='o', label="Uso de apps")
plt.plot(df_group.index, df_group["Screen_On_Time"], marker='o', label="Pantalla")

plt.title("Uso promedio del celular por edad")
plt.xlabel("Edad")
plt.ylabel("Tiempo (0 a 100)")
plt.legend()
plt.grid()

plt.show()