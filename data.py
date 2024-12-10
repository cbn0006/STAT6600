import netCDF4 as nc
import pandas as pd

# Load the .nc file
file_path = "data.nc"  # Replace with your actual file path
ds = nc.Dataset(file_path)

# Explore dataset to understand its structure
print(ds)

# Extract dimensions
lon = ds.variables['lon'][:]  # Longitude
lat = ds.variables['lat'][:]  # Latitude
sample_id = ds.variables['sample_id'][:]  # Sample ID

# Extract all variables
GSAT_hist_trd_model = ds.variables['GSAT_hist_trd_model'][:]  # 3D: sample_id, lat, lon
GSAT_hist_trd_obs = ds.variables['GSAT_hist_trd_obs'][:]  # 2D: lat, lon
GSAT_delta_model_near = ds.variables['GSAT_delta_model_near'][:]  # 1D: sample_id
GSAT_delta_model_mid = ds.variables['GSAT_delta_model_mid'][:]  # 1D: sample_id
GSAT_delta_model_long = ds.variables['GSAT_delta_model_long'][:]  # 1D: sample_id

# Create a list to store flattened data
data = []

# Flatten the data for DataFrame
for i, sample in enumerate(sample_id):
    for j, latitude in enumerate(lat):
        for k, longitude in enumerate(lon):
            # Handle 3D, 2D, and 1D variables
            GSAT_model = GSAT_hist_trd_model[i, j, k]
            GSAT_obs = GSAT_hist_trd_obs[j, k]  # Independent of sample_id
            GSAT_near = GSAT_delta_model_near[i]
            GSAT_mid = GSAT_delta_model_mid[i]
            GSAT_long = GSAT_delta_model_long[i]
            
            # Append a row with all variables
            data.append([
                sample, latitude, longitude, GSAT_model, GSAT_obs, GSAT_near, GSAT_mid, GSAT_long
            ])

# Define column names
columns = [
    'Sample_ID', 'Latitude', 'Longitude', 
    'GSAT_hist_trd_model', 'GSAT_hist_trd_obs', 
    'GSAT_delta_model_near', 'GSAT_delta_model_mid', 'GSAT_delta_model_long'
]

# Create DataFrame
df = pd.DataFrame(data, columns=columns)

# Save DataFrame to CSV
csv_file_path = "output.csv"  # Replace with desired output file name
df.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")
