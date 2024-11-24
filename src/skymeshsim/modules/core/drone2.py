"""Drone utilities module.

Author:
    Paulo Sanchez (@erlete)
"""


from .navigation import Orientation, Position


class Drone:
    """Preliminary drone class."""

    def __init__(self, position: Position, orientation: Orientation, speed: int | float, autonomy: int | float):
        self.position = position
        self.orientation = orientation
        self.speed = speed
        self.autonomy = autonomy
