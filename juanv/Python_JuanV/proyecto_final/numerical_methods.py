import numpy as np
from scipy.interpolate import CubicSpline


def centered_difference(y, dt):

    dy = np.zeros_like(y)

    dy[1:-1] = (y[2:] - y[:-2]) / (2 * dt)

    dy[0] = (y[1] - y[0]) / dt
    dy[-1] = (y[-1] - y[-2]) / dt

    return dy


def spline_interpolation(t, y):

    spline = CubicSpline(t, y)

    t_new = np.linspace(t.min(), t.max(), 3000)

    return t_new, spline(t_new)