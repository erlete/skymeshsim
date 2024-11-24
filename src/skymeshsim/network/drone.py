"""Drone module.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio
import json
import random
from typing import Optional, Tuple

from .logger import Logger
from .messages import (ClientIdentificationMessage, DroneStatusMessage,
                       LogMessage)
from .network_component import _BaseNetworkComponent
from .utils import geo_distance_to_m, predefined_route


class IndependentComponent(_BaseNetworkComponent):
    """Simulates a drone moving toward a target."""

    def __init__(self, id_: str, host: str, port: int, time_tick: float = 0.1, start_position: Tuple[float, float] = (-0.4, 39.4628)) -> None:
        super().__init__(host, port)

        self.id = id_
        self.time_tick = time_tick
        self.position = start_position
        self.target: Optional[Tuple[float, float]] = None

        self.waypoints = [(start_position[0] + x * 0.005, start_position[1] + y * 0.005)
                          for x, y in zip(predefined_route["x"], predefined_route["y"])]
        self.target = self.waypoints.pop(0)

        self._logger = Logger(1, f"[Drone ({self.id})]")

    async def run(self) -> None:
        """Connect to the server and process commands."""
        reader, writer = await asyncio.open_connection(self.host, self.port)

        await ClientIdentificationMessage(
            component=f"Drone-{self.id}",
            writer=writer
        ).send()

        asyncio.create_task(self.move(writer))

        try:
            while True:
                message = await reader.readline()

                if not message:
                    break

                decoded_message = json.loads(message.decode().strip())

                await LogMessage(
                    component=f"Drone-{self.id}",
                    message=f"Received: {decoded_message}",
                    writer=writer
                ).send()

                if (
                    decoded_message.get("type") == "dcmd"
                    and decoded_message.get("target") in (self.id, "all")
                    and decoded_message.get("command") == "moveto"
                ):
                    self.target = decoded_message.get("args")

        except asyncio.CancelledError:
            self._logger.log("Drone connection interrupted.", 2)

        finally:
            writer.close()
            await writer.wait_closed()

    async def move(self, writer: asyncio.StreamWriter) -> None:
        """Simulate movement toward the target."""
        while True:

            await DroneStatusMessage(
                component=f"Drone-{self.id}",
                location={
                    "x": self.position[0],
                    "y": self.position[1],
                    "z": 0.0
                },
                orientation={
                    "roll": 0.0,
                    "pitch": 0.0,
                    "yaw": 0.0
                },
                speed=random.random() * 10,
                autonomy=100 - random.random() * 10,
                writer=writer
            ).send()

            if self.target:
                tx, ty = self.target
                x, y = self.position
                dx, dy = tx - x, ty - y
                distance = geo_distance_to_m(x, y, tx, ty)

                print(
                    f"{tx = }, {ty = }, {x = }, {y = }, {dx = }, {dy = }, {distance = }")

                if distance < 10:  # 10 m offset
                    self.position = self.target
                    self.target = self.waypoints.pop(
                        0) if self.waypoints else None

                    await LogMessage(
                        component=f"Drone-{self.id}",
                        message=f"Reached {self.position}",
                        writer=writer
                    ).send()
                else:
                    step = self.time_tick * 50
                    print(f"{step = }")
                    self.position = (
                        x + step * dx / distance,
                        y + step * dy / distance
                    )
                    print(f"{self.position = }")

            await asyncio.sleep(self.time_tick)


if __name__ == "__main__":
    import sys

    drone_id = sys.argv[1]
    i = float(
        drone_id) if drone_id and drone_id is not None and drone_id.isnumeric() else 0
    print(i)
    drone = IndependentComponent(
        id_="1" if drone_id is None else drone_id,
        host="127.0.0.1",
        port=8888,
        time_tick=0.1,
        start_position=(-0.4 - 0.005 * i, 39.4628 + 0.001 * i)
    )

    asyncio.run(drone.run())
