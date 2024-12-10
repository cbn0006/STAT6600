import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def load_data(file_path):
    """
    Load the data from the CSV file and organize it into grids.
    """
    # Read the CSV file
    data = pd.read_csv(file_path)
    
    # Ensure Latitude and Longitude are sorted
    data = data.sort_values(by=['Latitude', 'Longitude'])
    
    return data

def get_grids(data, sample_id):
    """
    Extract modeled warming and observed warming grids for a specific sample ID.
    """
    # Filter the data for the given Sample_ID
    sample_data = data[data['Sample_ID'] == sample_id]
    
    if sample_data.empty:
        print(f"Sample ID {sample_id} not found in the dataset.")
        return None, None
    
    # Pivot tables to create 36x72 grids for modeled and observed warming
    modeled_warming = sample_data.pivot(index='Latitude', columns='Longitude', values='GSAT_hist_trd_model').values
    observed_warming = sample_data.pivot(index='Latitude', columns='Longitude', values='GSAT_hist_trd_obs').values
    
    return modeled_warming, observed_warming

def plot_grids(modeled_warming, observed_warming, sample_id):
    """
    Visualize the modeled warming, observed warming, and their difference using matplotlib.
    """
    # Calculate the difference
    difference = modeled_warming - observed_warming
    
    # Get the global min and max values for modeled and observed warming
    vmin_model_obs = min(modeled_warming.min(), observed_warming.min())
    vmax_model_obs = max(modeled_warming.max(), observed_warming.max())
    
    # Get the min and max values for the difference
    vmin_diff = difference.min()
    vmax_diff = difference.max()
    
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle(f"Sample ID: {sample_id} - Warming Visualization", fontsize=16)
    
    # Modeled warming heatmap
    im1 = axes[0].imshow(modeled_warming, cmap='coolwarm', aspect='auto', origin='lower', vmin=vmin_model_obs, vmax=vmax_model_obs)
    axes[0].set_title('Modeled Warming')
    axes[0].set_xlabel('Longitude')
    axes[0].set_ylabel('Latitude')
    fig.colorbar(im1, ax=axes[0], orientation='vertical', label='Modeled Warming')
    
    # Observed warming heatmap
    im2 = axes[1].imshow(observed_warming, cmap='coolwarm', aspect='auto', origin='lower', vmin=vmin_model_obs, vmax=vmax_model_obs)
    axes[1].set_title('Observed Warming')
    axes[1].set_xlabel('Longitude')
    axes[1].set_ylabel('Latitude')
    fig.colorbar(im2, ax=axes[1], orientation='vertical', label='Observed Warming')
    
    # Difference heatmap
    im3 = axes[2].imshow(difference, cmap='coolwarm', aspect='auto', origin='lower', vmin=vmin_diff, vmax=vmax_diff)
    axes[2].set_title('Difference (Modeled - Observed)')
    axes[2].set_xlabel('Longitude')
    axes[2].set_ylabel('Latitude')
    fig.colorbar(im3, ax=axes[2], orientation='vertical', label='Difference')
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()

def main():
    # File path to your CSV
    file_path = './output.csv'
    
    # Load the data
    data = load_data(file_path)
    
    # Input Sample_ID
    sample_id = int(input("Enter the Sample_ID: "))
    
    # Get the grids
    modeled_warming, observed_warming = get_grids(data, sample_id)
    
    if modeled_warming is not None and observed_warming is not None:
        # Plot the grids
        plot_grids(modeled_warming, observed_warming, sample_id)

if __name__ == "__main__":
    main()
