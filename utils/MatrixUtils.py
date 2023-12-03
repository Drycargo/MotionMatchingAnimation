import numpy as np
from enum import Enum


class Dir(Enum):
    X = 0
    Y = 1
    Z = 2


def getRotMat(angle, axis, useRad=False):
    if not useRad:
        angle = np.radians(angle)

    if axis == Dir.X:
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]])
    elif axis == Dir.Y:
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]])
    else:
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]])
