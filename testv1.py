import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show

# Load the dataset
file_path = "esp_pd_2020_1km.tif"  # Replace with your GeoTIFF file path
with rasterio.open(file_path) as dataset:
    # Display metadata
    print("Dataset Metadata:")
    print(f"Driver: {dataset.driver}")
    print(f"CRS: {dataset.crs}")
    print(f"Bounds: {dataset.bounds}")
    print(f"Width: {dataset.width}, Height: {dataset.height}")
    print(f"Number of Bands: {dataset.count}")
    print(f"Transform: {dataset.transform}")
    print(f"Data Type: {dataset.dtypes}")

    # Read the first band (or the only band if it's single-band)
    band1 = dataset.read(1)

# Calculate statistics
min_val = band1.min()
max_val = band1.max()
mean_val = band1.mean()
std_val = band1.std()
print("\nRaster Band Statistics:")
print(f"Min: {min_val}, Max: {max_val}, Mean: {mean_val}, Std: {std_val}")

# Plot the raster data with a colorbar
plt.figure(figsize=(10, 8))
img = plt.imshow(band1, cmap='viridis', vmin=min_val, vmax=max_val)
plt.colorbar(img, label="Raster Values")
plt.title("Raster Data Visualization")
plt.xlabel("Column Index")
plt.ylabel("Row Index")
plt.grid(False)
plt.show()

# Optional: Add geospatial visualization (e.g., overlaying on a map) using geopandas or folium.
