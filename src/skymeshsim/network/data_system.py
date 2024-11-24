"""Data system module.

Author:
    Paulo Sanchez (@erlete)
"""


import asyncio
import json
import math
import os
from typing import Any

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from matplotlib.colors import LinearSegmentedColormap, Normalize
from rasterio.mask import mask
from shapely.geometry import mapping

from .logger import Logger
from .messages import ClientIdentificationMessage
from .network_component import _BaseNetworkComponent
from .utils import COVER_RADIUS, radius_to_lat_lon_units


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
        """Start the plotting loop with terrain and population density, and update drone positions dynamically."""

        # Load Spain shapefile (for boundaries)
        spain_shapefile = gpd.read_file(os.path.join(
            os.path.dirname(__file__),
            "data",
            "ne_110m_admin_0_countries.shp"
        ))
        spain = spain_shapefile[spain_shapefile["ADMIN"] == "Spain"]
        spain = spain.to_crs("EPSG:4326")  # Ensure matching CRS for the data

        # Load the raster data for population density
        file_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "esp_pd_2020_1km.tif"
        )
        with rasterio.open(file_path) as dataset:
            out_image, out_transform = mask(
                dataset, [mapping(spain.geometry.iloc[0])], crop=True)
            out_meta = dataset.meta

        # Clamp the raster values to [0, inf)
        out_image = np.clip(out_image, 0, None)

        # Custom colormap (transparent to black with opacity)
        colors = [(0, (1, 1, 1, 0)), (1, (242 / 255, 107 / 255, 10 / 255, 1))]
        cmap_name = 'transparent_black'
        cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=100)

        # Plot the terrain and population density
        with rasterio.open(os.path.join(
            os.path.dirname(__file__),
            "data",
            "reprojected_terrain_view.tiff"
        )) as terrain_dataset:
            terrain_data = terrain_dataset.read([1, 2, 3])  # RGB bands
            terrain_transform = terrain_dataset.transform

        # Normalize reflectance to [0, 1]
        terrain_data = np.clip(terrain_data, 0, 10000) / 10000
        terrain_data = (terrain_data ** (1 / 1.5))  # Apply gamma correction
        # Convert to 0-255 range for display
        terrain_data = (terrain_data * 255).astype(np.uint8)

        # Set up the plot
        fig, ax = plt.subplots(1, 1)

        # Plot the terrain data (static)
        ax.imshow(np.transpose(terrain_data, (1, 2, 0)), extent=[
            terrain_transform[2],
            terrain_transform[2] + terrain_transform[0] *
            terrain_data.shape[2],
            terrain_transform[5] + terrain_transform[4] *
            terrain_data.shape[1],
            terrain_transform[5]
        ], alpha=1, zorder=3)

        # Plot population density (static)
        pop_density_data = np.squeeze(out_image)  # Remove extra dimensions
        ax.imshow(pop_density_data, cmap=cmap, extent=[
            out_transform[2],
            out_transform[2] + out_transform[0] * pop_density_data.shape[1],
            out_transform[5] + out_transform[4] * pop_density_data.shape[0],
            out_transform[5]
        ], alpha=1, norm=Normalize(vmin=pop_density_data.min(), vmax=pop_density_data.max()), zorder=4)

        # Plot the boundary of Spain (static)
        spain.boundary.plot(ax=ax, edgecolor="black",
                            facecolor=(0, 0, 0, .1), linewidth=1)

        # Add a colorbar for population density
        cbar = plt.colorbar(ax.imshow(pop_density_data, cmap=cmap),
                            ax=ax, orientation="vertical", fraction=0.036, pad=0.04)
        cbar.set_label("Population Density")

        # Add title and labels
        ax.set_title(
            "Drone Positions on Terrain and Population Density", fontsize=14)
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")

        # Create a scatter plot for the drone positions (this will be updated dynamically)
        sc = ax.scatter([], [], color=(237/255, 104/255, 95/255),
                        label='Drones', s=10, zorder=5)

        # Function to update both the position plot

        def update_plot() -> None:
            x_data = [data["location"]["x"]
                      for data in self.drone_data.values()]
            y_data = [data["location"]["y"]
                      for data in self.drone_data.values()]
            speeds = [data["speed"] for data in self.drone_data.values()]
            self._logger.log(
                f"Plotting drone positions: {x_data}, {y_data}", 0)
            self._logger.log(f"Plotting speeds: {speeds}", 0)

            if x_data and y_data:
                # Update the scatter plot for drone positions
                sc.set_offsets(list(zip(x_data, y_data)))

                # Dynamically adjust the plot limits for positions

                # ax.set_xlim(-0.5, -0.325)
                # ax.set_ylim(39.40, 39.52)
                # Plot circles around each drone position
                for x, y in zip(x_data, y_data):
                    circle_rad = radius_to_lat_lon_units(x, y, COVER_RADIUS)
                    circle = plt.Circle(
                        (x, y), circle_rad[0], color=(245/255, 182/255, 93/255, 0.05), fill=True, linestyle='--', linewidth=0.2, zorder=4)
                    ax.add_patch(circle)

            hardcoded_center = (-0.4, 39.48)
            margin = 0.05  # Add a margin to the bounds
            x_min, x_max = hardcoded_center[0] - \
                margin, hardcoded_center[0] + margin
            y_min, y_max = hardcoded_center[1] - \
                margin, hardcoded_center[1] + margin

            ax.set_xlim(x_min, x_max)
            ax.set_ylim(y_min, y_max)

        # Plotting loop (dynamic updates)
        while True:
            update_plot()  # Update the drone positions dynamically
            plt.pause(0.01)  # Non-blocking pause to refresh the plot
            await asyncio.sleep(0.01)  # Async sleep for non-blocking behavior


if __name__ == "__main__":
    data_system = DataSystem(host="127.0.0.1", port=8888)
    asyncio.run(data_system.run())
