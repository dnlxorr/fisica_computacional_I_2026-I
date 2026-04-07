import numpy as np
import matplotlib.pyplot as plt
import math

def f(x):
    return math.sin(x)

def taylor3(x):
    return x - (x**3)/math.factorial(3) + (x**5)/math.factorial(5)

def taylor6(x):
    return (x
            - (x**3)/math.factorial(3)
            + (x**5)/math.factorial(5)
            - (x**7)/math.factorial(7)
            + (x**9)/math.factorial(9)
            - (x**11)/math.factorial(11))

x = np.linspace(-3,3,200)

f_vals = [f(i) for i in x]
t3_vals = [taylor3(i) for i in x]
t6_vals = [taylor6(i) for i in x]

plt.plot(x,f_vals,label="sin(x)")
plt.plot(x,t3_vals,label="Taylor 3")
plt.plot(x,t6_vals,label="Taylor 6")

plt.legend()
plt.grid()

plt.xlabel("x")
plt.ylabel("y")

plt.title("Serie de Taylor")

plt.show()