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
# ena=True
# ena=False
def generate_csv():
    directory = "../PhysiCell/output_FADD_ko_o2_38/"
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
            # Convert the MATLAB data to a pandas DataFrame
            mat_data= mat_data[[0,7],:].astype(int)
            # Convert the MATLAB data to a pandas DataFrame
            df = pd.DataFrame(mat_data[1:], columns=mat_data[0],index = [timestep])
            timestep+=120
            data_frames.append(df)

    combined_df = pd.concat(data_frames,axis=0)
    combined_df.to_csv("cell_phases_with_o2.csv")
def plot():    
    print("mpika")
    combined_df = pd.read_csv("cell_phases_with_o2.csv",index_col=0).T

    category_counts = {}

    # Iterate over timepoints
    for timepoint in combined_df.columns:
        # Map cell phases to categories using the phases_dict and category_mapping
        category_data = combined_df[timepoint].map(phases_dict).map(phase_grouping)
        
        # Calculate the counts for each category in the current timepoint
        counts = category_data.value_counts()
        
        # Store the counts in the dictionary with the timepoint as the key
        category_counts[timepoint] = counts
        print(category_counts)

    # Create a DataFrame from the dictionary
    category_df = pd.DataFrame(category_counts).fillna(0)
    print(category_df)
    # Plot the time series 
    # with reversed axes
    category_df.T.plot(kind='line')
    plt.xlabel('Timepoints')
    plt.ylabel('Number of Cells')
    plt.title('Cell Category Time Series')
    plt.legend(title='Cell Category')
    plt.savefig('cell_phase.png')
    plt.show()
    

ena = int(sys.argv[1])
# generate_csv()
if ena:
    generate_csv()
else:
    plot()
