import numpy as np

# Dominio espacial

Nx = 120
Ny = 120

x = np.linspace(-3000, 3000, Nx)
y = np.linspace(-3000, 3000, Ny)

X, Y = np.meshgrid(x, y)


def generate_wave_field(X, Y, emitted_waves, c, current_time):

    Z = np.zeros_like(X)

    sigma = 100

    for x0, y0, t0 in emitted_waves:

        radius = c * (current_time - t0)

        if radius <= 0:
            continue

        r = np.sqrt((X - x0)**2 + (Y - y0)**2)

        wave = np.exp(
            -((r - radius)**2)/(2*sigma**2)
        )

        Z += wave

    return Z