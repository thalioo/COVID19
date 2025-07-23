"""
Combined COVID simulation analysis toolkit.
Includes:
- Extraction and CSV generation of cell phases/types from MATLAB and XML files
- Time series plotting of cell states/types
- Virion concentration visualization from simulation outputs
- Batch analysis of multiple simulation folders
"""
import os
import re
import xml.etree.ElementTree as ET
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as manimation
import matplotlib
from scipy.io import loadmat

# Dictionaries for cell phases and types
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
cell_type_dict = {1.0:'lung epithelium', 2.0:'immune', 3.0:'CD8 Tcell', 4.0:'macrophage', 5.0:'neutrophil', 6.0:'DC', 7.0:'CD4 Tcell', 8.0:'fibroblast'}


def get_cell_variable_names(xml_file):
    """
    Extracts cell variable names from a simulation XML file.
    """
    tree = ET.parse(xml_file)
    root = tree.getroot()
    simplified_blocks = root.findall(".//cell_population/custom/simplified_data")
    for block in simplified_blocks:
        if block.attrib.get("source") == "PhysiCell":
            labels = block.find("labels").findall("label")
            names = []
            for lbl in labels:
                size = int(lbl.attrib["size"])
                if size == 1:
                    names.append((int(lbl.attrib["index"]), lbl.text))
                else:
                    for i in range(size):
                        names.append((int(lbl.attrib["index"]), f"{lbl.text}_{i}"))
            return names
    return []

def load_mat_cell_values(cell_var_names, mat_path):
    """
    Loads cell data from a MATLAB file and returns a DataFrame with proper column names.
    """
    mat = scipy.io.loadmat(mat_path)
    cells = mat['cells'].T
    return pd.DataFrame(cells, columns=[y for _, y in cell_var_names])

def get_cell_means_for_dt(df):
    """
    Calculates counts of cell states (live, apoptotic, necrotic) for each cell type at a given timepoint.
    """
    df['phase_name'] = df['current_phase'].map(phases_dict)
    df['state'] = df['phase_name'].map(phase_grouping)
    df['cell_type_name'] = df['cell_type'].map(cell_type_dict)
    counts = df.groupby(['cell_type_name', 'state']).size().unstack(fill_value=0)
    for state in ['live', 'apoptotic', 'necrotic']:
        if state not in counts.columns:
            counts[state] = 0
    return counts[['live', 'apoptotic', 'necrotic']]

def extract_time_from_filename(filename):
    """
    Extracts the time index from a filename string.
    """
    match = re.search(r"output(\d+)", filename)
    return int(match.group(1)) if match else -1

def analyze_simulation_folder(folder_path, label=None):
    """
    Processes all output files in a simulation folder, returning a DataFrame of cell state counts over time.
    """
    xml_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".xml")], key=extract_time_from_filename)
    cell_var_names = get_cell_variable_names(os.path.join(folder_path, xml_files[0]))
    results = []
    time = 0
    for xml_file in xml_files:
        mat_file = xml_file.replace(".xml", "_cells_physicell.mat")
        mat_path = os.path.join(folder_path, mat_file)
        if not os.path.exists(mat_path):
            continue
        df = load_mat_cell_values(cell_var_names, mat_path)
        counts = get_cell_means_for_dt(df)
        counts["time"] = time
        counts["sim"] = label if label else os.path.basename(folder_path)
        time+=1
        results.append(counts.reset_index())
    return pd.concat(results, ignore_index=True)

def plot_cell_states_over_time(df, cell_types=None):
    """
    Plots time series of cell states for each cell type and simulation.
    """
    if cell_types is None:
        cell_types = df["cell_type_name"].unique()
    states = ["live", "apoptotic", "necrotic"]
    sim_ids = df["sim"].unique()
    for cell_type in cell_types:
        plt.figure(figsize=(10, 5))
        for sim in sim_ids:
            sim_df = df[(df["cell_type_name"] == cell_type) & (df["sim"] == sim)].sort_values("time")
            for state in states:
                plt.plot(sim_df["time"], sim_df[state], label=f"{sim} - {state}")
        plt.title(f"Cell States Over Time - {cell_type}")
        plt.xlabel("Time step")
        plt.ylabel("Count")
        plt.legend()
        plt.tight_layout()
        plt.show()
        plt.savefig(f"time_series_{cell_type}.png", dpi=300)

def analyze_all_simulations(parent_folder):
    """
    Processes all simulation folders in a parent directory, returning a combined DataFrame.
    """
    sim_data = []
    for sim_folder in sorted(os.listdir(parent_folder)):
        sim_path = os.path.join(parent_folder, sim_folder, "output")
        if os.path.isdir(sim_path):
            print(f"Analyzing {sim_folder}...")
            df = analyze_simulation_folder(sim_path, label=sim_folder)
            sim_data.append(df)
    return pd.concat(sim_data, ignore_index=True)

def plot_epithelial_counts_all_sims(df, save_path="epithelial_states_all_sims.png", show=False):
    """
    Plots time series of epithelial cell states for all simulations.
    """
    df_epithelial = df[df["cell_type_name"] == "lung epithelium"]
    states = ["live", "apoptotic", "necrotic"]
    plt.figure(figsize=(12, 6))
    for sim in df_epithelial["sim"].unique():
        sim_df = df_epithelial[df_epithelial["sim"] == sim].sort_values("time")
        for state in states:
            plt.plot(sim_df["time"], sim_df[state], label=f"{sim} - {state}")
    plt.title("Epithelial Cell States Over Time (All Simulations)")
    plt.xlabel("Time Step")
    plt.ylabel("Cell Count")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    if show:
        plt.show()
    else:
        plt.close()

def generate_csv_from_mat(directory, phase_col=7, out_name="cell_phases.csv"):
    """
    Generates a CSV file of cell phases or types over time from MATLAB files in a simulation output directory.
    phase_col: column index for phase/type (7 for phase, 5 for type)
    """
    directory = os.path.join(directory, "output")
    timestep = 0
    data_frames = []
    for filename in sorted(os.listdir(directory)):
        if filename.endswith("cells_physicell.mat") and filename.startswith("output"):
            file_path = os.path.join(directory, filename)
            mat_data = loadmat(file_path)['cells']
            mat_data = mat_data[[0, phase_col], :].astype(int)
            df = pd.DataFrame(mat_data[1:], columns=mat_data[0], index=[timestep])
            timestep += 120
            data_frames.append(df)
    combined_df = pd.concat(data_frames, axis=0)
    combined_df.to_csv(os.path.join(directory, out_name))
    return combined_df

def plot_time_series_from_csv(csv_path, mapping_dict, grouping_dict=None, drop_cols=None, out_png="plot.png"):
    """
    Plots time series from a CSV file, mapping values using mapping_dict and optionally grouping with grouping_dict.
    """
    df = pd.read_csv(csv_path, index_col=0).T
    category_counts = {}
    for timepoint in df:
        category_data = df[timepoint].map(mapping_dict)
        if grouping_dict:
            category_data = category_data.map(grouping_dict)
        counts = category_data.value_counts()
        category_counts[timepoint] = counts
    category_df = pd.DataFrame(category_counts).fillna(0).T
    if drop_cols:
        category_df = category_df.drop(columns=drop_cols)
    category_df.plot(kind='line')
    plt.xlabel('Timepoints')
    plt.ylabel('Number of Cells')
    plt.title('Time Series')
    plt.legend(title='Category')
    plt.savefig(out_png)
    plt.show()

def visualize_virion_concentration(instance_folder, xml_config_path, n_frames=481):
    """
    Visualizes virion concentration over time from simulation output XML files, saves frames as PNGs.
    No dependency on pyMCDS; parses XML files directly.
    """
    import xml.etree.ElementTree as ET
    output_data = os.path.join(instance_folder, 'output')
    matplotlib.rc('xtick', labelsize=10)
    matplotlib.rc('ytick', labelsize=10)
    matplotlib.rc('figure', figsize=[8,8])
    os.makedirs(os.path.join(output_data, 'concentrations'), exist_ok=True)
    for index in range(n_frames):
        filename = f'output{index:08d}.xml'
        xml_path = os.path.join(output_data, filename)
        if not os.path.exists(xml_path):
            continue
        tree = ET.parse(xml_path)
        root = tree.getroot()
        # Extract mesh info
        microenv = root.find('.//microenvironment')
        if microenv is None:
            print(f"No microenvironment found in {filename}")
            continue
        # Get mesh
        mesh = microenv.find('mesh')
        x_coords = np.array([float(x.text) for x in mesh.find('x_coordinates').findall('x')])
        y_coords = np.array([float(y.text) for y in mesh.find('y_coordinates').findall('y')])
        # Get substrate data
        substrates = microenv.find('substrate')
        virion_idx = None
        # Find virion index
        for i, sub in enumerate(microenv.findall('substrate')):
            if sub.attrib.get('name', '').lower() == 'virion':
                virion_idx = i
                break
        if virion_idx is None:
            print(f"No virion substrate found in {filename}")
            continue
        # Get concentrations
        substrate = microenv.findall('substrate')[virion_idx]
        concentration = np.array([float(c.text) for c in substrate.find('bulk').findall('concentration')])
        # Reshape to grid
        nx, ny = len(x_coords), len(y_coords)
        oxygen = concentration.reshape((nx, ny))
        X, Y = np.meshgrid(x_coords, y_coords, indexing='ij')
        plt.clf()
        im = plt.contourf(X, Y, oxygen)
        plt.axis('image')
        plt.ticklabel_format(style='plain', axis='both')
        fmt = '%1.2f'
        plt.colorbar(im, format=fmt)
        plt.title(f'{instance_folder} timepoint: {index * 30}')
        plt.savefig(os.path.join(output_data, 'concentrations', f'{index * 30}.png'))
        plt.close()

# Example usage (uncomment and edit paths as needed):
# df_all = analyze_all_simulations("experiments/grande/")
# plot_epithelial_counts_all_sims(df_all, save_path="epithelial_comparison.png")
# visualize_virion_concentration("/path/to/instance_folder", "config/set_deb.xml")
