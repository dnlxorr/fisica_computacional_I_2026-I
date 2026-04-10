import pandas as pd
import matplotlib.pyplot as plt

url = "https://raw.githubusercontent.com/Mikhthad/Mobile-Device-Usage-and-User-Behavior-Dataset/main/user_behavior_dataset.csv"
df = pd.read_csv(url)

# Tomar solo una muestra para que no se vea lleno
df_sample = df.sample(100)

plt.figure()
plt.scatter(df_sample["App_Usage_Time"], df_sample["Screen_On_Time"])

plt.title("Relación entre uso de apps y tiempo de pantalla")
plt.xlabel("Uso de apps (0 a 100)")
plt.ylabel("Pantalla (0 a 100)")
plt.grid()

plt.show()