import xml.etree.ElementTree as ET
import scipy.io
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os,re
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

def get_cell_variable_names(xml_file):
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
    mat = scipy.io.loadmat(mat_path)
    cells = mat['cells'].T
    return pd.DataFrame(cells, columns=[y for _, y in cell_var_names])

def get_cell_means_for_dt(df):
    df['phase_name'] = df['current_phase'].map(phases_dict)
    df['state'] = df['phase_name'].map(phase_grouping)
    df['cell_type_name'] = df['cell_type'].map(cell_type_dict)
    counts = df.groupby(['cell_type_name', 'state']).size().unstack(fill_value=0)
    for state in ['live', 'apoptotic', 'necrotic']:
        if state not in counts.columns:
            counts[state] = 0
    return counts[['live', 'apoptotic', 'necrotic']]

def extract_time_from_filename(filename):
    match = re.search(r"output(\d+)", filename)
    return int(match.group(1)) if match else -1

def analyze_simulation_folder(folder_path, label=None):
    xml_files = sorted([f for f in os.listdir(folder_path) if f.endswith(".xml")], key=extract_time_from_filename)
    cell_var_names = get_cell_variable_names(os.path.join(folder_path, xml_files[0]))

    results = []
    time = 0
    for xml_file in xml_files:
        # time = extract_time_from_filename(xml_file)
        mat_file = xml_file.replace(".xml", "_cells_physicell.mat")
        mat_path = os.path.join(folder_path, mat_file)
        if not os.path.exists(mat_path):
            continue
        df = load_mat_cell_values(cell_var_names, mat_path)
        counts = get_cell_means_for_dt(df)
        counts["time"] = time
        counts["sim"] = label if label else os.path.basename(folder_path)
        # print(counts)
        time+=1
        results.append(counts.reset_index())

    return pd.concat(results, ignore_index=True)

def plot_cell_states_over_time(df, cell_types=None):
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
        plt.savefig("time_series"+str(cell_type)+".png", dpi=300)
def analyze_all_simulations(parent_folder):
    sim_data = []
    for sim_folder in sorted(os.listdir(parent_folder)):
        sim_path = os.path.join(parent_folder, sim_folder, "output")
        if os.path.isdir(sim_path):
            print(f"Analyzing {sim_folder}...")
            df = analyze_simulation_folder(sim_path, label=sim_folder)
            sim_data.append(df)
    return pd.concat(sim_data, ignore_index=True)

def plot_epithelial_counts_all_sims(df, save_path="epithelial_states_all_sims.png", show=False):
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
# df_single = analyze_simulation_folder("experiments/grande/instance_15/output")
# plot_cell_states_over_time(df_single)

df_all = analyze_all_simulations("experiments/grande/")
plot_epithelial_counts_all_sims(df_all, save_path="epithelial_comparison.png")