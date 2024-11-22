import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from shapely.geometry import mapping

# Load Spain shapefile
spain_shapefile = gpd.read_file("ne_110m_admin_0_countries.shp")
spain = spain_shapefile[spain_shapefile["ADMIN"] == "Spain"]

# Reproject Spain's geometry to match the raster CRS (EPSG:4326)
spain = spain.to_crs("EPSG:4326")

# Load the population density raster data
file_path = "esp_pd_2020_1km.tif"  # Replace with your file path
with rasterio.open(file_path) as dataset:
    # Clip the raster using Spain's boundary
    out_image, out_transform = mask(
        dataset, [mapping(spain.geometry.iloc[0])], crop=True)
    out_meta = dataset.meta

# Clamp the raster values to [0, inf)
out_image = np.clip(out_image, 0, None)

# Update metadata for the clipped raster
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

# Load the terrain data
terrain_file_path = "spain_dem.tif"  # Replace with your file path
with rasterio.open(terrain_file_path) as terrain_dataset:
    # Clip the terrain raster using Spain's boundary
    terrain_image, terrain_transform = mask(
        terrain_dataset, [mapping(spain.geometry.iloc[0])], crop=True)
    terrain_meta = terrain_dataset.meta

# Clamp the terrain raster values to [0, inf)
terrain_image = np.clip(terrain_image, 0, None)

# Update metadata for the clipped terrain raster
terrain_meta.update({
    "driver": "GTiff",
    "height": terrain_image.shape[1],
    "width": terrain_image.shape[2],
    "transform": terrain_transform
})

# Plot the raster over Spain's map
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Plot the terrain data
terrain_data = np.squeeze(terrain_image)  # Remove extra dimensions
terrain_img = ax.imshow(
    terrain_data, cmap="terrain", extent=[
        terrain_transform[2],
        terrain_transform[2] + terrain_transform[0] * terrain_data.shape[1],
        terrain_transform[5] + terrain_transform[4] * terrain_data.shape[0],
        terrain_transform[5]
    ],
    alpha=0.7  # Transparency for better overlay
)

# Plot the population density data
raster_data = np.squeeze(out_image)  # Remove extra dimensions
raster_img = ax.imshow(
    raster_data, cmap="viridis", extent=[
        out_transform[2],
        out_transform[2] + out_transform[0] * raster_data.shape[1],
        out_transform[5] + out_transform[4] * raster_data.shape[0],
        out_transform[5]
    ],
    alpha=0.5  # Transparency for better overlay
)

# Plot Spain's boundary
spain.boundary.plot(ax=ax, edgecolor="red", linewidth=1)

# Add colorbars
cbar = plt.colorbar(raster_img, ax=ax, orientation="vertical",
                    fraction=0.036, pad=0.04)
cbar.set_label("Population Density")

terrain_cbar = plt.colorbar(terrain_img, ax=ax, orientation="vertical",
                            fraction=0.036, pad=0.04)
terrain_cbar.set_label("Terrain Elevation")

# Add title and labels
ax.set_title("Population Density and Terrain Elevation over Spain", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
