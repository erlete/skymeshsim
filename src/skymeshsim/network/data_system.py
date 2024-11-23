"""Data system module.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio
import json
from typing import Any

import matplotlib.pyplot as plt

from .logger import Logger
from .messages import ClientIdentificationMessage
from .network_component import _BaseNetworkComponent


class DataSystem(_BaseNetworkComponent):
    """Logs messages received from the server and plots drone data."""

    def __init__(self, host: str, port: int):
        super().__init__(host, port)
        self.drone_data: dict[str, Any] = {}

        self._logger = Logger(1, "[DataSystem]")

    async def run(self) -> None:
        """Connect to the server and log messages."""
        reader, writer = await asyncio.open_connection(self.host, self.port)
        await ClientIdentificationMessage(
            component="DataSystem",
            writer=writer
        ).send()

        # Start the plotting in a separate task
        asyncio.create_task(self.start_plotting())

        try:
            while True:
                message = await reader.readline()

                if not message:
                    break

                self._logger.log(f"Received: {message.decode().strip()}", 0)

                try:
                    # Decode and parse the JSON message
                    decoded_message = json.loads(message.decode().strip())

                    if decoded_message["type"] == "dronestatus":
                        self._logger.log(f"Drone status: {decoded_message}", 0)
                        self.update_drone_data(decoded_message)

                except json.JSONDecodeError:
                    self._logger.log("Received invalid JSON.", 2)

        except asyncio.CancelledError:
            self._logger.log("DataSystem interrupted.", 1)

    def update_drone_data(self, message) -> None:
        """Update the drone data with the received message."""
        self.drone_data[message.get("component")] = {
            "location": message["location"],
            "orientation": message["orientation"],
            "speed": message["speed"],
            "autonomy": message["autonomy"],
        }

    async def start_plotting(self) -> None:
        """Start the plotting loop."""
        _, ax = plt.subplots()
        sc = ax.scatter([], [])
        ax.set_title("Drone Positions")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        def update_plot() -> None:
            x_data = [data["location"]["x"]
                      for data in self.drone_data.values()]
            y_data = [data["location"]["y"]
                      for data in self.drone_data.values()]
            self._logger.log(f"Plotting: {x_data}, {y_data}", 0)

            if x_data and y_data:
                sc.set_offsets(list(zip(x_data, y_data)))

                # Dynamically adjust the plot limits
                margin = 1.0  # Add a margin to the bounds
                x_min, x_max = min(x_data) - margin, max(x_data) + margin
                y_min, y_max = min(y_data) - margin, max(y_data) + margin

                ax.set_xlim(x_min, x_max)
                ax.set_ylim(y_min, y_max)

        # Plotting loop
        while True:
            update_plot()
            plt.pause(0.1)  # Non-blocking pause to refresh the plot
            await asyncio.sleep(0.1)  # Async sleep for 1 second

# Example usage:
# data_system = DataSystem('localhost', 8888)
# asyncio.run(data_system.run())


if __name__ == "__main__":
    data_system = DataSystem(host="127.0.0.1", port=8888)
    asyncio.run(data_system.run())
