import asyncio
import json
import random
from typing import Optional, Tuple

from .messages import (ClientIdentificationMessage, ConnectionChangeMessage,
                       DroneStatusMessage, LogMessage)
from .network_component import _BaseNetworkComponent


class IndependentComponent(_BaseNetworkComponent):
    """Simulates a drone moving toward a target."""

    def __init__(self, id_: str, host: str, port: int, time_tick: float = 0.1):
        super().__init__(host, port)

        self.id = id_
        self.time_tick = time_tick
        self.position = (0.0, 0.0)
        self.target: Optional[Tuple[float, float]] = None

    async def run(self) -> None:
        """Connect to the server and process commands."""
        reader, writer = await asyncio.open_connection(self.host, self.port)

        await ClientIdentificationMessage(
            component=f"Drone-{self.id}",
            writer=writer
        ).send()

        asyncio.create_task(self.move(writer))

        print("connected")

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

                if decoded_message.get("type") == "cmd" and decoded_message.get("command") == "moveto":
                    self.target = decoded_message.get("target")

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
                speed=0.0,
                autonomy=100,
                writer=writer
            ).send()

            if self.target:
                tx, ty = self.target
                x, y = self.position
                dx, dy = tx - x, ty - y
                distance = (dx ** 2 + dy ** 2) ** 0.5

                if distance < 0.1:
                    self.position = self.target
                    self.target = None

                    await LogMessage(
                        component=f"Drone-{self.id}",
                        message=f"Reached {self.position}",
                        writer=writer
                    ).send()
                else:
                    step = self.time_tick * 1.0
                    self.position = (
                        x + step * dx / distance,
                        y + step * dy / distance
                    )

                    # Add random variation to the position
                    variation_x = (random.random() - 0.5) * 0.1
                    variation_y = (random.random() - 0.5) * 0.1
                    self.position = (
                        self.position[0] + variation_x,
                        self.position[1] + variation_y
                    )

            await asyncio.sleep(self.time_tick)


if __name__ == "__main__":
    import sys

    drone_id = sys.argv[1]
    drone = IndependentComponent(
        id_="1" if drone_id is None else drone_id,
        host="127.0.0.1",
        port=8888,
        time_tick=0.1
    )

    asyncio.run(drone.run())
