"""Navigation classes module.

Author:
    Paulo Sanchez (@erlete)
"""


class Position:
    """Preliminary position class."""

    def __init__(self, x: int | float, y: int | float, z: int | float):
        self.x = x
        self.y = y
        self.z = z


class Orientation:
    """Preliminary orientation class."""

    def __init__(self, pitch: int | float, roll: int | float, yaw: int | float):
        self.pitch = pitch
        self.roll = roll
        self.yaw = yaw
