from scipy.io import loadmat
import os,glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

cell_type_dict = {1.0:'lung epithelium',
                  2.0:'immune',
                  3.0:'CD8 Tcell',
                  4.0:'macrophage',
                  5.0:'neutrophil',
                  6.0:'DC',
                  7.0:'CD4 Tcell',
                  8.0:'fibroblast'}

directory = "./_FADD_ko/"
timestep = 0
data_by_time = {}
data_frames = [] 

for filename in sorted(os.listdir(directory)):
    if filename.endswith("cells_physicell.mat") and filename.startswith("output"):
        file_path = os.path.join(directory, filename)
        print(file_path)
        # Load the .mat file
        mat_data = loadmat(file_path)
        
        mat_data = mat_data['cells']
        mat_data= mat_data[[0,5],:].astype(int)
        # Convert the MATLAB data to a pandas DataFrame
        df = pd.DataFrame(mat_data[1:], columns=mat_data[0],index = [timestep])

        # df = df.astype(int)
        # df = df.T
        # df.columns = [timestep]

        # print(df)
        # grouped = df.groupby(0)  # Replace with actual column name
        # cell_counts = grouped.size()
        # Store the grouped data for this time step
        # data_by_time[timestep] = cell_counts.to_dict()
        timestep+=60
        data_frames.append(df)
        # if timestep >160:
        #     break
combined_df = pd.concat(data_frames,axis=0)
combined_df.to_csv("cell_types.csv")

# cell_types = set()
# for time_point_data in data_by_time.values():
#     cell_types.update(time_point_data.keys())

# # Set up the plot
# plt.figure(figsize=(12, 6))

# # Plot each cell type as a separate line
# for cell_type in cell_types:
#     cell_counts = []
#     for time_point_data in data_by_time.values():
#         cell_counts.append(time_point_data.get(cell_type, 0))
#     plt.plot(data_by_time.keys(), cell_counts, label=f'{cell_type_dict[cell_type]}')

# plt.xlabel('Time Points')
# plt.ylabel('Number of Cells')
# plt.title('Number of Cells by Cell Type Over Time')
# plt.legend()
# plt.tight_layout()
# print(data_by_time)
# # Show the plot
# plt.savefig(directory+'cell_type_plot.png')

# plt.show()
