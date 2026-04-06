
import pandas as pd
import matplotlib.pyplot as plt


ruta = r'C:\Users\lezly\OneDrive - Universidad de Pamplona\Documents\computacional_I\12720.csv'
df = pd.read_csv(ruta, sep=';', decimal=',')


df_total = df[df['Convocatoria de la prueba de acceso a la universidad'] == 'Total']
presentados = df_total[df_total['Concepto Educativo'] == 'Estudiantes presentados']
aprobados = df_total[df_total['Concepto Educativo'] == 'Estudiantes aprobados']


fig, axs = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Análisis Comparativo: Mujeres en Acceso Universitario', fontsize=16)


axs[0, 0].plot(presentados['Periodo'], presentados['Total'], color='blue', label='Presentadas')
axs[0, 0].plot(aprobados['Periodo'], aprobados['Total'], color='red', linestyle='--', label='Aprobadas')
axs[0, 0].set_title('1. Gráfica de Líneas')
axs[0, 0].legend()


axs[0, 1].scatter(presentados['Periodo'], presentados['Total'], color='blue', label='Presentadas')
axs[0, 1].scatter(aprobados['Periodo'], aprobados['Total'], color='red', marker='x', label='Aprobadas')
axs[0, 1].set_title('2. Gráfica de Dispersión (Scatter)')
axs[0, 1].legend()



axs[1, 0].scatter(presentados['Periodo'], presentados['Total'], s=300, color='blue', alpha=0.3)
axs[1, 0].scatter(aprobados['Periodo'], aprobados['Total'], s=300, color='red', alpha=0.3)
axs[1, 0].set_title('3. Gráfica de Densidad (Alpha Overlay)')


axs[1, 1].plot(presentados['Periodo'], presentados['Total'], 'b.', markersize=10)
axs[1, 1].plot(aprobados['Periodo'], aprobados['Total'], 'r.', markersize=10)
axs[1, 1].set_title('4. Gráfica de Puntos (Dot Plot)')


for ax in axs.flat:
    ax.set_xlabel('Año')
    ax.set_ylabel('Porcentaje (%)')
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.invert_xaxis()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()




