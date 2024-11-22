import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.mask import mask
from rasterio.plot import show
from shapely.geometry import mapping

# Load Spain shapefile
# Replace this with the path to your shapefile or use Geopandas built-in datasets
spain_shapefile = gpd.read_file("ne_110m_admin_0_countries.shp")
spain = spain_shapefile[spain_shapefile["ADMIN"] == "Spain"]

# Reproject Spain's geometry to match the raster CRS (EPSG:4326)
spain = spain.to_crs("EPSG:4326")

# Load the raster data
file_path = "esp_pd_2020_1km.tif"  # Replace with your file path
with rasterio.open(file_path) as dataset:
    # Clip the raster using Spain's boundary
    out_image, out_transform = mask(
        dataset, [mapping(spain.geometry.iloc[0])], crop=True)
    out_meta = dataset.meta

# Update metadata for the clipped raster
out_meta.update({
    "driver": "GTiff",
    "height": out_image.shape[1],
    "width": out_image.shape[2],
    "transform": out_transform
})

# Plot the raster over Spain's map
fig, ax = plt.subplots(1, 1, figsize=(10, 8))

# Plot the raster data
raster_data = np.squeeze(out_image)  # Remove extra dimensions
raster_img = ax.imshow(
    raster_data, cmap="viridis", extent=[
        out_transform[2],
        out_transform[2] + out_transform[0] * raster_data.shape[1],
        out_transform[5] + out_transform[4] * raster_data.shape[0],
        out_transform[5]
    ],
    alpha=0.7  # Transparency for better overlay
)

# Plot Spain's boundary
spain.boundary.plot(ax=ax, edgecolor="red", linewidth=1)

# Add a colorbar
cbar = plt.colorbar(raster_img, ax=ax, orientation="vertical",
                    fraction=0.036, pad=0.04)
cbar.set_label("Population Density")

# Add title and labels
ax.set_title("Population Density over Spain", fontsize=14)
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

plt.show()
