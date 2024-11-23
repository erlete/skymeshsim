import asyncio
import json
from typing import Optional, Tuple

from .messages import LogMessage
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
        writer.write(f"Drone-{self.id}\n".encode())
        await writer.drain()

        asyncio.create_task(self.move(writer))

        try:
            while True:
                message = await reader.readline()

                if not message:
                    break
                decoded_message = json.loads(
                    message.decode().strip())  # Decode JSON message

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

    def parse_target(self, message: dict) -> Tuple[float, float]:
        """Parse target coordinates from the command."""
        x, y = message.get("target", (0.0, 0.0))
        return x, y

    async def move(self, writer: asyncio.StreamWriter) -> None:
        """Simulate movement toward the target."""
        while True:
            await writer.drain()
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

            await asyncio.sleep(self.time_tick)


if __name__ == "__main__":
    drone = IndependentComponent(
        id_="1", host="127.0.0.1", port=8888, time_tick=0.1)
    drone2 = IndependentComponent(
        id_="2", host="127.0.0.1", port=8888, time_tick=0.1)
    asyncio.run(drone.run())
    asyncio.run(drone2.run())
