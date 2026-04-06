import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("dielectron.csv")

print(data.head())
plt.figure()

plt.hist(data["M"], bins=100)

plt.xlabel("Invariant Mass M")
plt.ylabel("Frequency")
plt.title("Distribution of Dielectron Invariant Mass")

plt.show()