"""Drone API module.

Author:
    Paulo Sanchez (@erlete)
"""


from ..geometry.drone import Drone
from .vector import Rotator3D, Vector3D


class DroneAPI(Drone):
    """Drone API class.

    This class represents a kinematic drone model, implementing the geometry
    of the drone and adding a speed attribute to it.

    Attributes:
        drone (Drone): drone.
        speed (float): drone speed in m/s.
        SPEED_RANGE (tuple[int, int]): allowed drone speed range in m/s.
    """

    SPEED_RANGE = (0, 200)  # [m/s]

    def __init__(
        self,
        position: Vector3D,
        rotation: Rotator3D,
        speed: int | float = 0
    ) -> None:
        """Initialize a DroneAPI instance.

        Args:
            position (Vector3D): drone position.
            rotation (Rotator3D): drone rotation.
            speed (int | float): drone speed in m/s.
        """
        super().__init__(position, rotation)
        self.speed = speed

    @property
    def speed(self) -> float:
        """Get drone speed.

        Returns:
            float: drone speed.
        """
        return self._speed

    @speed.setter
    def speed(self, value: int | float) -> None:
        """Set drone speed.

        Args:
            value (int | float): drone speed.
        """
        if not isinstance(value, (int, float)):
            raise TypeError(
                "expected type float for"
                + f" {self.__class__.__name__}.speed but got"
                + f" {type(value).__name__} instead"
            )

        self._speed = float(
            max(self.SPEED_RANGE[0], min(value, self.SPEED_RANGE[1]))
        )

    def __repr__(self) -> str:
        """Get short drone representation.

        Returns:
            str: short drone representation.
        """
        return f"<DroneAPI at {self._position}>"

    def __str__(self) -> str:
        """Get long drone representation.

        Returns:
            str: long drone representation.
        """
        return f"""DroneAPI(
    position={self._position},
    rotation={self._rotation},
    speed={self._speed}
)"""
