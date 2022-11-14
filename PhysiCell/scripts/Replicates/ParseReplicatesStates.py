#!/usr/bin/env python
# coding: utf-8

# In[1]:

import scipy.io as sio
import numpy as np
import os
import sys
import argparse
import csv
os.chdir('../../')
sys.path.append('.')
from pyMCDS import pyMCDS
import matplotlib.pyplot as plt
parser = argparse.ArgumentParser(description='Process input')
parser.add_argument('--folder', type=str, default="", help='Choose which results to analyse')
parser.add_argument('--replicates', type=int, default=12, help='Inform how many replicated where done')

args = parser.parse_args()


counts = []

# Here we are storing all the existing states for each cell type
# state_dict = {}
count_dict = {}

nb_timesteps = 0
for j in range(args.replicates): 
    
    if len(args.folder) > 0:
        path = os.path.join(args.folder, 'output_R'+str("%02d"%j))
    else:
        path = 'output_R'+str("%02d"%j)


    nb_timesteps = 0
    while os.path.exists(os.path.join(path, 'output{:08d}.xml'.format(nb_timesteps))):
        nb_timesteps += 1
    
    for k in range(nb_timesteps):


        
        str_name = 'output{:08d}.xml'.format(k)
        
        mcds = pyMCDS(str_name, path)  # /case1/run3/output

        
        type_by_id = dict(zip(
            mcds.data['discrete_cells']['ID'].astype(int), 
            mcds.data['discrete_cells']['cell_type'].astype(int)
        ))
        types = mcds.data['discrete_cells']['cell_type'].astype(int)

        list_types = list(set(types))
        
        # count_dict = {type_id : {} for type_id in list_types}

        for celltype in list_types:
            if celltype not in count_dict.keys():
                count_dict.update({celltype: {}})
            
            # if celltype not in state_dict.keys():
            #     state_dict.update({celltype: []})

        with open(os.path.join(path, 'states_%08u.csv' % k), newline='') as csvfile:
            states_reader = csv.reader(csvfile, delimiter=',')
        
            for row in states_reader:
                if row[0] != 'ID':
                    t_id = int(row[0])
                    state = row[1]

                    if state not in count_dict[type_by_id[t_id]]:
                        count_dict[type_by_id[t_id]][state] = [np.zeros((args.replicates, 1)) for _ in range(nb_timesteps)]
                    else:
                        count_dict[type_by_id[t_id]][state][k][j] += 1

                    # if state not in state_dict[type_by_id[t_id]]:
                    #     state_dict[type_by_id[t_id]].append(state)
        # print(count_dict)

# print(state_dict)
trajs_by_celltype = {}
errors_by_celltype = {}
for celltype, data in count_dict.items():

    error_by_state = {}
    traj_by_state = {}
    for state, values in data.items():

        ks = []
        es = []
        for k in range(nb_timesteps):
            ks.append(np.mean(values[k]))
            es.append(np.std(values[k]))
        
        traj_by_state.update({state:np.array(ks)})
        error_by_state.update({state:np.array(es)})
    
    trajs_by_celltype.update({celltype: traj_by_state})
    errors_by_celltype.update({celltype: error_by_state})


plt.plot(range(nb_timesteps), trajs_by_celltype[1]["<nil>"])
plt.fill_between(range(nb_timesteps), 
                trajs_by_celltype[1]["<nil>"] - errors_by_celltype[1]["<nil>"],
                trajs_by_celltype[1]["<nil>"] + errors_by_celltype[1]["<nil>"],
                color='C0', alpha=0.35
)  
plt.tight_layout()
if len(args.folder) > 0:
    plt.savefig(os.path.join(args.folder, 'states_epitelials.png'), dpi=600, pad_inches=0.1, bbox_inches='tight')  # dpi=600, 
else:
    plt.savefig('states_epitelials.png', dpi=600, pad_inches=0.1, bbox_inches='tight')  # dpi=600, 



plt.plot(range(nb_timesteps), trajs_by_celltype[4]["Active"])
plt.fill_between(range(nb_timesteps), 
                trajs_by_celltype[4]["Active"] - errors_by_celltype[4]["Active"],
                trajs_by_celltype[4]["Active"] + errors_by_celltype[4]["Active"],
                color='C0', alpha=0.35
)
plt.tight_layout()
if len(args.folder) > 0:
    plt.savefig(os.path.join(args.folder, 'states_macrophages.png'), dpi=600, pad_inches=0.1, bbox_inches='tight')  # dpi=600, 
else:
    plt.savefig('states_macrophages.png', dpi=600, pad_inches=0.1, bbox_inches='tight')  # dpi=600, 
