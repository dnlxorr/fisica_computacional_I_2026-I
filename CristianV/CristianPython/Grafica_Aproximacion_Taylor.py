import numpy as np
import math as m
import matplotlib.pyplot as plt

# Funcion de la funcion original
def funOrg (x):
    return np.sin(x)

# Funcion de aproximacion por Taylor con 3 terminos
def funAprox1 (x):
    return x - (x**3)/m.factorial(3) + (x**5)/m.factorial(5)

# Funcion de aproximacion por Taylor con 6 terminos
def funAprox2 (x):
    return x - (x**3)/m.factorial(3) + (x**5)/m.factorial(5) - (x**7)/m.factorial(7) + (x**9)/m.factorial(9) - (x**11)/m.factorial(11)

def ECM1(x):
    ecm1 = np.mean((funOrg(x) - funAprox1(x))**2)
    return ecm1

def ECM2(x):
    ecm2 = np.mean((funOrg(x) - funAprox2(x))**2)
    return ecm2

x = np.linspace(-3,3 ,500)
plt.plot(x,funOrg(x), label="Org", linestyle="--", linewidth=3)
plt.plot(x,funAprox1(x), label="Aprox1")
plt.plot(x,funAprox2(x), label="Aprox2")

plt.legend(['Org','Aprox1','Aprox2'])
plt.grid(True)
plt.title(f"Grafico de Taylor de x \n  ECM Orden 3: {ECM1(x):.5f} | ECM Orden 6: {ECM2(x):.5f} ")
plt.xlabel('x')
plt.ylabel('y')

print(ECM1(x))
print(ECM2(x))
plt.show()