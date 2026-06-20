import numpy as np

GAMMA = 1.4
R = 287.0


def speed_of_sound(T_celsius):
    """
    Velocidad del sonido en función de la temperatura.
    """
    T_kelvin = T_celsius + 273.15
    return np.sqrt(GAMMA * R * T_kelvin)


def aircraft_velocity(v0, a, t):
    return v0 + a * t


def aircraft_position(x0, v0, a, t):
    return x0 + v0 * t + 0.5 * a * t**2


def mach_number(v, c):
    return v / c


def doppler_frequency(f0, c, v, approaching=True):

    eps = 1e-6

    if approaching:
        denom = max(c - v, eps)
        return f0 * c / denom

    return f0 * c / (c + v)