import numpy as np
import matplotlib.pyplot as plt


m = 3.0          # kg
F = 10.0         # N
vi = 7.0         # m/s
vf_obj = 30.0    # m/s
a_val = F / m    # 3.33 m/s^2

# Tiempo y paso
t_final = (vf_obj - vi) / a_val
n = 40
t = np.linspace(0, t_final, n + 1)
h = t[1] - t[0]


acel = np.full_like(t, a_val)


v_trap = [vi]
v_simp = [vi]
for i in range(n):
    v_trap.append(v_trap[-1] + (h/2)*(acel[i] + acel[i+1]))
    if i % 2 == 0 and i < n-1:
        p = (h/3)*(acel[i] + 4*acel[i+1] + acel[i+2])
        v_simp.append(v_simp[-1] + (h/2)*(acel[i] + acel[i+1])) # punto medio
        v_simp.append(v_simp[-1 - 1] + p)

# POSICIÓN (Integral de la Velocidad)
# Usamos v_trap como base para integrar la posición
p_trap = [0.0]
p_simp = [0.0]
for i in range(n):
    p_trap.append(p_trap[-1] + (h/2)*(v_trap[i] + v_trap[i+1]))
    if i % 2 == 0 and i < n-1:
        p = (h/3)*(v_trap[i] + 4*v_trap[i+1] + v_trap[i+2])
        p_simp.append(p_simp[-1] + (h/2)*(v_trap[i] + v_trap[i+1]))
        p_simp.append(p_simp[-1 - 1] + p)

# Ajustar longitudes por el método de Simpson
v_simp = np.array(v_simp[:len(t)])
p_simp = np.array(p_simp[:len(t)])
v_trap = np.array(v_trap)
p_trap = np.array(p_trap)



def generar_reporte(t, datos_trap, datos_simp, titulo_gen, unidad, color):

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)
    fig.suptitle(f'ANÁLISIS DE {titulo_gen}', fontsize=14, fontweight='bold')


    ax1.plot(t, datos_trap, 'o--', color='orange', label='Método Trapecio')
    ax1.set_ylabel(f'{unidad}')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_title("Integración por Regla del Trapecio")


    ax2.plot(t, datos_simp, '-', color=color, label='Método Simpson', linewidth=2)
    ax2.set_ylabel(f'{unidad}')
    ax2.legend(loc='upper left')
    ax2.grid(True, alpha=0.3)
    ax2.set_title("Integración por Regla de Simpson 1/3")


    error = datos_trap - datos_simp
    ax3.fill_between(t, error, color='red', alpha=0.2, label='Diferencia (T - S)')
    ax3.plot(t, error, color='red', linewidth=1)
    ax3.set_ylabel('Diferencia')
    ax3.set_xlabel('Tiempo (s)')
    ax3.legend(loc='upper left')
    ax3.grid(True, linestyle=':')
    ax3.set_title("Error Relativo entre Métodos")

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])


generar_reporte(t, acel, acel, 'ACELERACIÓN', 'm/s²', 'red')


generar_reporte(t, v_trap, v_simp, 'VELOCIDAD', 'm/s', 'blue')


generar_reporte(t, p_trap, p_simp, 'POSICIÓN', 'm', 'green')

plt.show()