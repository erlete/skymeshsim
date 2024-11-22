import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask
from shapely.geometry import mapping

# Load Spain shapefile
spain_shapefile = gpd.read_file("ne_110m_admin_0_countries.shp")
spain = spain_shapefile[spain_shapefile["ADMIN"] == "Spain"]
spain = spain.to_crs("EPSG:4326")  # Match CRS of raster

# Load population density raster
pop_density_path = "esp_pd_2020_1km.tif"
with rasterio.open(pop_density_path) as pop_dataset:
    pop_image, pop_transform = mask(
        pop_dataset, [mapping(spain.geometry.iloc[0])], crop=True)
    pop_meta = pop_dataset.meta

# Load terrain data raster
terrain_path = "spain_dem.tif"  # Replace with your terrain data path
with rasterio.open(terrain_path) as terrain_dataset:
    terrain_image, terrain_transform = mask(
        terrain_dataset, [mapping(spain.geometry.iloc[0])], crop=True)
    terrain_meta = terrain_dataset.meta

    # Resample terrain to match population density resolution
    terrain_resampled = np.empty_like(pop_image)
    rasterio.warp.reproject(
        source=terrain_image,
        destination=terrain_resampled,
        src_transform=terrain_transform,
        src_crs=terrain_dataset.crs,
        dst_transform=pop_transform,
        dst_crs=pop_dataset.crs,
        resampling=rasterio.warp.Resampling.bilinear,
    )

# Normalize and scale terrain data for visualization
terrain_resampled = np.squeeze(terrain_resampled)  # Remove extra dimensions
terrain_scaled = (terrain_resampled - np.min(terrain_resampled)) / (
    np.max(terrain_resampled) - np.min(terrain_resampled)
)

# Create a combined visualization
fig, ax = plt.subplots(1, 1, figsize=(12, 8))

# Overlay the terrain (scaled) with transparency
ax.imshow(
    terrain_scaled,
    cmap="terrain",
    extent=[
        pop_transform[2],
        pop_transform[2] + pop_transform[0] * terrain_scaled.shape[1],
        pop_transform[5] + pop_transform[4] * terrain_scaled.shape[0],
        pop_transform[5],
    ],
    alpha=0.5,  # Set transparency
)

# Overlay the population density raster
pop_image = np.squeeze(pop_image)  # Remove extra dimensions
pop_img = ax.imshow(
    pop_image,
    cmap="viridis",
    extent=[
        pop_transform[2],
        pop_transform[2] + pop_transform[0] * pop_image.shape[1],
        pop_transform[5] + pop_transform[4] * pop_image.shape[0],
        pop_transform[5],
    ],
    alpha=0.6,  # Set transparency
)

# Add Spain's boundary
spain.boundary.plot(ax=ax, edgecolor="red", linewidth=1)

# Add a colorbar for terrain data
cbar_terrain = plt.colorbar(
    pop_img, ax=ax, orientation="vertical", fraction=0.036, pad=0.04)
cbar_terrain.set_label("Population Density")

# Add a title and labels
ax.set_title("Population Density and Terrain Overlay", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
