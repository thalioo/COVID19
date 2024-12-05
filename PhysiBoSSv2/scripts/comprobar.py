import numpy as np
from scipy.io import loadmat





import os
import numpy as np
import pandas as pd
from scipy.io import loadmat

# Directory containing the .mat files
directory = '/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/data/PhysiBoSSv2/output_test/'  # Update this to your directory
file_prefix = 'output00000'
file_suffix = '_cells_physicell.mat'
row_indices = [0, 5, 6, 7, 90]
# Prepare a DataFrame to hold all the data
all_data = pd.DataFrame()

# Loop through the files in the specified range
for i in range(5):  # Assuming files range from 000 to 999
    file_num = f'{i:03}'  # Format number as 3 digits with leading zeros
    file_name = f'{file_prefix}{file_num}{file_suffix}'
    file_path = os.path.join(directory, file_name)
    print(file_num)
    if os.path.exists(file_path):
        # Load the .mat file
        mat_data = loadmat(file_path)
        
        # Assuming the numpy array is under a known key, e.g., 'data'
        data = mat_data['cells']  # Update the key based on your .mat file structure
        
        # Extract specific rows
        extracted_data = data[row_indices, :]
        
        # Convert the first row (ID) to a single row, and remaining to columns
        ids = extracted_data[0, :]
        states = extracted_data[1:, :]
        
        # Create a DataFrame with IDs as columns
        df = pd.DataFrame(states.T, columns=['state_5', 'state_6', 'state_7', 'state_90'])
        df['id'] = ids
        df['timepoint'] = int(file_num)*30  # Add the file number for identification
        
        # Append to the overall DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)
    else:
        print(f"File {file_name} not found.")

# Save the combined data to a CSV file
output_csv = 'combined_output.csv'
all_data.to_csv(output_csv, index=False)
print(f"Data saved to {output_csv}")
