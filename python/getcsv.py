import sys
import os
import json
import re
import xml.etree.ElementTree as ET
from scipy.io import loadmat
import numpy as np
import pandas as pd


def convert_mat_to_csv(instance_folder):
    # Map cell type codes to names from central.xml
    celltype_dict = {
        0: "default",
        1: "lung_epithelium",
        2: "immune",
        3: "CD8_Tcell",
        4: "macrophage",
        5: "neutrophil",
        6: "DC",
        7: "CD4_Tcell",
        8: "fibroblast",
        9: "residual"
    }
    cm_dic = {4: "alive", 100: "apoptotic", 101: "necrotic"}
    output_data = instance_folder +"/output/"
    data = []
    print(output_data)
    index=0
    for filename in sorted(os.listdir(output_data)):
        
        if filename.endswith("cells_physicell.mat") and filename.startswith("output"):
            file_path = os.path.join(output_data, filename)
        else:
            continue
        instance = {}

        mcds = loadmat(file_path)
        ct = mcds['cells'][5]
        cp = mcds['cells'][6]
        vir_arr = mcds['cells'][90]
        all_cells = len(ct)
        instance["timepoint"] = index * 30  # Time in minutes (assuming 30-minute intervals)
        instance['num_all_cells'] = all_cells

        unique_types = np.unique(ct)
        for cell_type in unique_types:
            type_indices = [i for i, t in enumerate(ct) if t == cell_type]
            celltype_name = celltype_dict.get(cell_type, f"type_{cell_type}")
            instance[f'num_total_{celltype_name}'] = len(type_indices)
            type_phases = [cp[i] for i in type_indices]
            unique_phases, counts = np.unique(type_phases, return_counts=True)
            count_dict = dict(zip(unique_phases, counts))
            instance[f'num_alive_{celltype_name}'] = count_dict.get(6, 0)
            instance[f'num_apoptotic_{celltype_name}'] = count_dict.get(100, 0)
            instance[f'num_necrotic_{celltype_name}'] = count_dict.get(101, 0)
            infected = [vir_arr[i] for i in type_indices if vir_arr[i] >= 1]
            instance[f'num_infected_{celltype_name}'] = len(infected)
        # from filename remove cells_physicell and add 0
        microenv_filename = filename.replace("_cells_physicell","_microenvironment0")
        file_path= os.path.join(output_data, microenv_filename)
        env = loadmat(file_path)["multiscale_microenvironment"]

        virion = np.mean(env[4,:])
        cytokine = np.mean(env[6,:])
        ros = np.mean(env[13,:])
        instance['virion']=virion
        instance['cytokine']=cytokine
        instance['ros']= ros
        data.append(instance)
        index += 1
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(instance_folder, "output.csv"), index=False)

if __name__ == "__main__":
    convert_mat_to_csv(sys.argv[1])
