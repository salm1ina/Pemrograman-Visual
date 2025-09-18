import numpy as np
import matplotlib.pyplot as plt

# batas integrasi
a, b = 0, 3
N = 1000 

# fungsi
def f(x):
    return x**2

# Step 1. generate Data untuk Kurva Fungsi
x_vals = np.linspace(a, b, 500)
y_vals = f(x_vals)

# titik acak (Monte Carlo)
x_random = np.random.uniform(a, b, N)
y_random = np.random.uniform(0, b**2, N)  # batas atas y diambil dari max(x^2) = b^2

# pisahkan titik di bawah kurva (inside) dan di atas kurva (outside)
inside_x = x_random[y_random <= f(x_random)]
inside_y = y_random[y_random <= f(x_random)]

outside_x = x_random[y_random > f(x_random)]
outside_y = y_random[y_random > f(x_random)]

# Step 2. Plot Kurva Fungsi dan Titik Acak
plt.figure(figsize=(10, 5))

# Plot kurva f(x) = x^2
plt.plot(x_vals, y_vals, color='skyblue', linewidth=2, label='f(x) = x^2')

# plot titik random
plt.scatter(inside_x, inside_y, color='blue', s=10, alpha=0.2, label='Inside (Under Curve)')
plt.scatter(outside_x, outside_y, color='yellow', s=10, alpha=0.2, edgecolor='black', label='Outside (Above Curve)')

plt.title("Monte Carlo Simulation: Visualization")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()