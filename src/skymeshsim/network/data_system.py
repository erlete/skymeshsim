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

                    if decoded_message["type"] == "dstat":
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
        """Start the plotting loop with two subplots: one for drone positions and one for speed."""
        # Create a figure with two subplots: one for drone positions and one for speed
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

        # Scatter plot for drone positions
        sc = ax1.scatter([], [])
        ax1.set_title("Drone Positions")
        ax1.set_xlabel("Longitude")
        ax1.set_ylabel("Latitude")

        # Bar plot for drone speeds
        bar_width = 0.35
        drone_ids = []  # List to store drone IDs
        speed_bars = ax2.bar([], [], width=bar_width)
        ax2.set_title("Drone Speeds")
        ax2.set_xlabel("Drone ID")
        ax2.set_ylabel("Speed (m/s)")

        # Function to update both the position and speed plots
        def update_plot() -> None:
            x_data = [data["location"]["x"]
                      for data in self.drone_data.values()]
            y_data = [data["location"]["y"]
                      for data in self.drone_data.values()]
            speeds = [data["speed"] for data in self.drone_data.values()]
            self._logger.log(f"Plotting positions: {x_data}, {y_data}", 0)
            self._logger.log(f"Plotting speeds: {speeds}", 0)

            if x_data and y_data:
                # Update the scatter plot for drone positions
                sc.set_offsets(list(zip(x_data, y_data)))

                # Dynamically adjust the plot limits for positions
                margin = 1.0  # Add a margin to the bounds
                x_min, x_max = min(x_data) - margin, max(x_data) + margin
                y_min, y_max = min(y_data) - margin, max(y_data) + margin

                ax1.set_xlim(x_min, x_max)
                ax1.set_ylim(y_min, y_max)

            if speeds:
                # Update the bar plot for drone speeds
                ax2.clear()  # Clear previous bars to avoid overlap
                ax2.bar(drone_ids, speeds, width=bar_width)
                # Adjust y-axis to fit speed data
                ax2.set_ylim(0, max(speeds) + 1)

                # Re-add labels and title after clearing
                ax2.set_title("Drone Speeds")
                ax2.set_xlabel("Drone ID")
                ax2.set_ylabel("Speed (m/s)")

        # Plotting loop
        while True:
            # Update drone IDs list for the bar plot
            drone_ids = list(self.drone_data.keys())
            update_plot()  # Update both plots
            plt.pause(0.1)  # Non-blocking pause to refresh the plot
            await asyncio.sleep(0.1)  # Async sleep for non-blocking behavior
# Example usage:
# data_system = DataSystem('localhost', 8888)
# asyncio.run(data_system.run())


if __name__ == "__main__":
    data_system = DataSystem(host="127.0.0.1", port=8888)
    asyncio.run(data_system.run())
