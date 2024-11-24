"""Drone representation module.

Author:
    Paulo Sanchez (@erlete)
"""


import numpy as np

from ..core.vector import Rotator3D, Vector3D


class Drone:
    """Drone representation class.

    Attributes:
        position (Vector3D): drone position.
        rotation (Rotator3D): drone rotation.
    """

    STRUCTURE = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1]
    ])

    SURFACE = np.array([
        [0, 1, 3, 2],
        [4, 5, 7, 6],
        [0, 1, 5, 4],
        [2, 3, 7, 6],
        [0, 2, 6, 4],
        [1, 3, 7, 5]
    ])

    def __init__(self, position: Vector3D, rotation: Rotator3D) -> None:
        """Initialize a Drone instance.

        Args:
            position (Vector3D): drone position.
            rotation (Rotator3D): drone rotation.
        """
        self.position = position
        self.rotation = rotation

    @property
    def position(self) -> Vector3D:
        """Get drone position.

        Returns:
            Vector3D: drone position.
        """
        return self._position

    @position.setter
    def position(self, value: Vector3D) -> None:
        """Set drone position.

        Args:
            value (Vector3D): drone position.
        """
        if not isinstance(value, Vector3D):
            raise TypeError(
                "expected type Vector3D for"
                + f" {self.__class__.__name__}.position but got"
                + f" {type(value).__name__} instead"
            )

        self._position = value

    @property
    def rotation(self) -> Rotator3D:
        """Get drone rotation.

        Returns:
            Rotator3D: drone rotation.
        """
        return self._rotation

    @rotation.setter
    def rotation(self, value: Rotator3D) -> None:
        """Set drone rotation.

        Args:
            value (Rotator3D): drone rotation.
        """
        if not isinstance(value, Rotator3D):
            raise TypeError(
                "expected type Rotator3D for"
                + f" {self.__class__.__name__}.rotation but got"
                + f" {type(value).__name__} instead"
            )

        self._rotation = value

    def plot(self, ax) -> None:
        """Plot drone.

        Args:
            ax (Axes3D): ax to plot drone on.
        """
        print("Warning: Drone.plot() has not been implemented yet.")
        return None

    def __repr__(self) -> str:
        """Get short drone representation.

        Returns:
            str: short drone representation.
        """
        return f"<Drone at {self._position}>"

    def __str__(self) -> str:
        """Get long drone representation.

        Returns:
            str: long drone representation.
        """
        return f"""Drone(
    position={self._position},
    rotation={self._rotation}
)"""
