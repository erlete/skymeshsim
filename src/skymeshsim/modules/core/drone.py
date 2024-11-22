from .navigation import Position


class Drone:

    def __init__(self, position: Position, energy: int | float):
        self.position = position
        self.energy = energy

    def __repr__(self):
        return f"Drone(position={self.position}, energy={self.energy})"

    def __str__(self):
        return f"Drone at {self.position} with {self.energy} energy"
