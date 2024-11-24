"""Simulation API module.

This module combines all API resources to compose the Simulation API,
responsible for the execution and update of the simulation.

Author:
    Paulo Sanchez (@erlete)
"""


import numpy as np

from .drone import DroneAPI as Drone
from .vector import Rotator3D, Vector3D


class SimulationAPI:
    """Simulation API class.

    This class represents a simulation that implements all kinematic variants
    of the simulation elements, such as the drone and the track. It provides
    with several methods that allow the user to get information about the
    simulation's state and control it.

    Attributes:
        tracks (list[TrackAPI]): track list.
        drone (DroneAPI): drone element.
        next_waypoint (Vector3D | None): next waypoint data.
        remaining_waypoints (int): remaining waypoints in the track.
        is_simulation_finished (bool): whether the simulation is finished.
        DT (float): simulation time step in seconds.
        DV (float): simulation speed step in m/s.
        DR (float): simulation rotation step in rad/s.
    """

    DT = 0.1  # [s]
    DV = 7.5  # [m/s]
    DR = np.pi  # [rad/s]

    SUMMARY_FILE_PREFIX = "summary_"
    SUMMARY_DIR = "statistics"

    def __init__(self, drone: Drone) -> None:
        """Initialize a SimulationAPI instance.

        Args:
            tracks (list[Track]): track list.
        """
        self._drone = drone
        self._current_timer = 0.0
        self._timeout = 9999

        self._target_rotation = Rotator3D(0, 0, 0)
        self._target_speed = 0.0
        self._is_simulation_finished = False

    @property
    def drone(self) -> Drone:
        """Returns the drone element.

        Returns:
            DroneAPI: drone element.
        """
        return self._drone

    @property
    def is_simulation_finished(self) -> bool:
        """Returns whether the simulation is finished.

        Returns:
            bool: True if the simulation is finished, False otherwise.
        """
        return self._is_simulation_finished

    def set_drone_target_state(
        self,
        yaw: int | float,
        pitch: int | float,
        speed: int | float
    ) -> None:
        """Set drone target state.

        Args:
            yaw (int | float): target drone yaw in radians.
            pitch (int | float): target drone pitch in radians.
            speed (int | float): target drone speed in m/s.
        """
        if not isinstance(yaw, (int, float)):
            raise TypeError(
                "expected type (int, float) for"
                + f" {self.__class__.__name__}.set_drone_target_state yaw"
                + f" but got {type(yaw).__name__} instead"
            )

        if not isinstance(pitch, (int, float)):
            raise TypeError(
                "expected type (int, float) for"
                + f" {self.__class__.__name__}.set_drone_target_state pitch"
                + f" but got {type(pitch).__name__} instead"
            )

        if not isinstance(speed, (int, float)):
            raise TypeError(
                "expected type int | float for"
                + f" {self.__class__.__name__}.set_drone_target_state speed"
                + f" but got {type(speed).__name__} instead"
            )

        self._target_rotation = Rotator3D(
            np.rad2deg(yaw),
            np.rad2deg(pitch),
            0
        )
        self._target_speed = speed

    def update(self) -> None:
        """Update drone state along the current track and plot environment.

        Args:
            plot (bool): whether to plot statistics after each track. Defaults
                to True.
            dark_mode (bool): whether to use dark mode for the plot. Defaults
                to False. Only used if plot is True.
            fullscreen (bool): whether to plot the figure in fullscreen mode.
                Defaults to True. Only used if plot is True.
        """
        self._current_timer += self.DT

        if self._current_timer >= self._timeout:
            self._is_simulation_finished = True

            return

        # Rotation update:
        self.drone.rotation = Rotator3D(
            *[
                np.rad2deg(
                    min(curr_rot + self.DR * self.DT, tg_rot)
                    if curr_rot < tg_rot else
                    max(curr_rot - self.DR * self.DT, tg_rot)
                ) for curr_rot, tg_rot in zip(
                    self.drone.rotation,
                    self._target_rotation
                )
            ]
        )

        # Speed update:
        speed = self.drone.speed
        self.drone.speed = (
            min(speed + self.DV * self.DT, self._target_speed)
            if self._target_speed >= speed else
            max(speed - self.DV * self.DT, self._target_speed)
        )

        # Position update:
        rot = self.drone.rotation
        self.drone.position += (
            Vector3D(
                speed * self.DT * np.cos(rot.x) * np.cos(rot.y),
                speed * self.DT * np.sin(rot.x) * np.cos(rot.y),
                speed * self.DT * np.sin(rot.y)
            )
        )
