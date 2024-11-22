import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from rasterio.windows import from_bounds
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

print({
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

# Coordenadas del bounding box de Valencia (manual o calculadas)
# Coordenadas aproximadas (lon_min, lat_min, lon_max, lat_max)
coords_top = [39.557822, -0.538444]
coords_bottom = [39.362120, -0.222607]

valencia_bbox = [coords_top[1], coords_top[0],
                 coords_bottom[1], coords_bottom[0]]

# Recortar datos de población
with rasterio.open(file_path) as dataset:
    valencia_window = from_bounds(*valencia_bbox, transform=dataset.transform)
    valencia_pop = dataset.read(1, window=valencia_window)
    valencia_transform = dataset.window_transform(valencia_window)

# Recortar datos de terreno
with rasterio.open(terrain_file_path) as terrain_dataset:
    valencia_window_terrain = from_bounds(
        *valencia_bbox, transform=terrain_dataset.transform)
    valencia_terrain = terrain_dataset.read(1, window=valencia_window_terrain)
    valencia_transform_terrain = terrain_dataset.window_transform(
        valencia_window_terrain)


# Plot Valencia
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Plot terrain data for Valencia
terrain_img = ax.imshow(
    valencia_terrain, cmap="terrain", extent=[
        valencia_bbox[0], valencia_bbox[2], valencia_bbox[1], valencia_bbox[3]
    ], alpha=0.7
)

# Plot population density data for Valencia
pop_img = ax.imshow(
    valencia_pop, cmap="viridis", extent=[
        valencia_bbox[0], valencia_bbox[2], valencia_bbox[1], valencia_bbox[3]
    ], alpha=0.5
)

# Add colorbars
cbar = plt.colorbar(pop_img, ax=ax, orientation="vertical",
                    fraction=0.036, pad=0.04)
cbar.set_label("Population Density")

terrain_cbar = plt.colorbar(
    terrain_img, ax=ax, orientation="vertical", fraction=0.036, pad=0.04)
terrain_cbar.set_label("Terrain Elevation")

# Add title and labels
ax.set_title(
    "Population Density and Terrain Elevation over Valencia", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
