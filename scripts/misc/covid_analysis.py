from scipy.io import loadmat
import os,glob,sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


phases_dict = {
    0: "Ki67_positive_premitotic",
    1: "Ki67_positive_postmitotic",
    2: "Ki67_positive",
    3: "Ki67_negative",
    4: "G0G1_phase",
    5: "G0_phase",
    6: "G1_phase",
    7: "G1a_phase",
    8: "G1b_phase",
    9: "G1c_phase",
    10: "S_phase",
    11: "G2M_phase",
    12: "G2_phase",
    13: "M_phase",
    14: "live",
    100: "apoptotic",
    101: "necrotic_swelling",
    102: "necrotic_lysed",
    103: "necrotic",
    104: "debris"
    }
phase_grouping = { 
    "Ki67_positive_premitotic": "live",  
    "Ki67_positive_postmitotic": "live", 
    "Ki67_positive": "live", 
    "Ki67_negative": "live", 
    "G0G1_phase": "live", 
    "G0_phase": "live", 
    "G1_phase": "live", 
    "G1a_phase": "live", 
    "G1b_phase": "live", 
    "G1c_phase": "live", 
    "S_phase": "live", 
    "G2M_phase": "live", 
    "G2_phase": "live", 
    "M_phase": "live", 
    "live": "live", 
    "apoptotic": "apoptotic",  
    "necrotic_lysed": "necrotic", 
    "necrotic": "necrotic",
    "necrotic_swelling": "necrotic"
    }
cell_type_dict = {1.0:'lung epithelium',
                  2.0:'immune',
                  3.0:'CD8 Tcell',
                  4.0:'macrophage',
                  5.0:'neutrophil',
                  6.0:'DC',
                  7.0:'CD4 Tcell',
                  8.0:'fibroblast'}

def generate_csv(directory):
    directory = directory+"output/"
    timestep = 0
    data_by_time = {}
    data_frames = [] 
    for filename in sorted(os.listdir(directory)):
        if filename.endswith("cells_physicell.mat") and filename.startswith("output"):
            file_path = os.path.join(directory, filename)
            # Load the .mat file
            mat_data = loadmat(file_path)
            mat_data = mat_data['cells']
            # Convert the MATLAB data to a pandas DataFrame
            mat_data= mat_data[[0,7],:].astype(int)
            # Convert the MATLAB data to a pandas DataFrame
            df = pd.DataFrame(mat_data[1:], columns=mat_data[0],index = [timestep])
            timestep+=120
            data_frames.append(df)

    combined_df = pd.concat(data_frames,axis=0)
    combined_df.to_csv(directory+"/cell_phases.csv")
    return combined_df
def plot_single(data=None, file_path=None,directory=None):
    if file_path:   
        combined_df = pd.read_csv(directory+"/output/cell_phases.csv",index_col=0).T
    else:
        combined_df=data
    category_counts = {}
    print(combined_df)
    # Iterate over timepoints
    for timepoint in combined_df.columns:
        # Map cell phases to categories using the phases_dict and category_mapping
        category_data = combined_df[timepoint].map(phases_dict).map(phase_grouping)
        
        # Calculate the counts for each category in the current timepoint
        counts = category_data.value_counts()
        
        # Store the counts in the dictionary with the timepoint as the key
        category_counts[timepoint] = counts

    # Create a DataFrame from the dictionary
    category_df = pd.DataFrame(category_counts).fillna(0)
    # Plot the time series 
    # with reversed axes
    category_df.T.plot(kind='line')
    plt.xlabel('Timepoints')
    plt.ylabel('Number of Cells')
    plt.title('Cell Category Time Series')
    plt.legend(title='Cell Category')
    plt.savefig(directory+'/cell_phase.png')
    plt.show()
    
def generate_cell_types_csv(directory):
    timestep = 0
    data_by_time = {}
    data_frames = [] 
    directory = directory+"output/"
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

            timestep+=120
            data_frames.append(df)
            # if timestep >160:
            #     break
    combined_df = pd.concat(data_frames,axis=0)
    combined_df.to_csv(directory+"/cell_types.csv")

def plot_single_types(data=None, file_path=None,directory=None):
    if file_path:   
        combined_df = pd.read_csv(directory+"/output/cell_types.csv",index_col=0).T

    else:
        combined_df=data
    category_counts = {}


    # Iterate over timepoints
    for timepoint in combined_df:
        # Map cell phases to categories using the phases_dict and category_mapping
        category_data = combined_df[timepoint].map(cell_type_dict)
        
        # Calculate the counts for each category in the current timepoint
        counts = category_data.value_counts()
        
        # Store the counts in the dictionary with the timepoint as the key
        category_counts[timepoint] = counts
    category_df = pd.DataFrame(category_counts).fillna(0).T
    print(category_df)
    category_df = category_df.drop(columns=['lung epithelium'])

    category_df.plot(kind='line')
    plt.xlabel('Timepoints')
    plt.ylabel('Number of Cells')
    plt.title('Cell Type Time Series')
    plt.legend(title='Cell Types')
    plt.savefig(directory+'/cell_types.png')
    plt.show()
    return
i="/gpfs/scratch/bsc08/bsc008602/emews_output/covid_moi_02_dep_not_immune_whole_gp/instance_226/"
generate_csv(i)
generate_cell_types_csv(i)
plot_single(file_path=i,directory = i)
plot_single_types(file_path=i,directory = i)
# exp_folder = "experiments/exp_12/"
# # generate_cell_types_csv(exp_folder+"instance_1/output")
# os.chdir(exp_folder)
# updated_directory = os.getcwd()
# # print("Updated Directory:", updated_directory)
# for i in glob.glob(updated_directory+"/instance_*/"):
#     print(i)
#     # generate_csv(i)
#     # generate_cell_types_csv(i)
#     plot_single(file_path=i,directory = i)
#     plot_single_types(file_path=i,directory = i)
