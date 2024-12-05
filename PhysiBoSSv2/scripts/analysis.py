# import sys
# sys.path.append("../exp_original/pyMCDS.py")

from pyMCDS import pyMCDS
import numpy as np
import matplotlib.pyplot as plt 

cm_dic = {6:"alive",100:"apoptotic",101:"necrotic"}
# filename is xml filename without the path of the output
alive_counts = {}
apoptotic_counts = {}
necrotic_counts = {}
cell_counts = {}
inf_cells = {}
for index in range(0,10):
    # 
    filename ='output%08u.xml' % index
    print(filename)
    mcds = pyMCDS(filename)
    ct = mcds.data['discrete_cells']['cell_type']
    all_cells = len(ct)
    cell_counts[index*15]=all_cells
    cp = mcds.data['discrete_cells']['cycle_model']
    target_indices = [index for index, cell_type in enumerate(ct) if cell_type == 1]
    target_cell_phases = [cp[index] for index in target_indices]
    unique, counts = np.unique(target_cell_phases, return_counts=True)
    count_dict = dict(zip(unique, counts))
    alive_counts[index*15]=count_dict.get(6, 0)
    apoptotic_counts[index*15]=count_dict.get(100, 0)
    necrotic_counts[index*15]=count_dict.get(101, 0)
    vir_arr = mcds.data['discrete_cells']['virion']
    infected = vir_arr >= 1
    inf_cells[index*15]=(len(np.where(infected)[0]))
print(inf_cells)
    
# print(necrotic_counts)
plt.figure()
# plt.plot(alive_counts.keys(), alive_counts.values(), label='Alive')
plt.plot(apoptotic_counts.keys(), apoptotic_counts.values(), label='apoptotic')
plt.plot(necrotic_counts.keys(), necrotic_counts.values(), label='necrotic')

plt.xlabel('time')
plt.ylabel('Cell Count')
plt.legend()
plt.savefig("dead_counts.png")
plt.clf()


plt.figure()
plt.plot(alive_counts.keys(), alive_counts.values(), label='Alive')
plt.plot(apoptotic_counts.keys(), apoptotic_counts.values(), label='apoptotic')
plt.plot(necrotic_counts.keys(), necrotic_counts.values(), label='necrotic')

plt.xlabel('time')
plt.ylabel('Cell Count')
plt.legend()
plt.savefig("cell_counts.png")
plt.clf()
# max_count = max(max(alive_counts.values()), max(apoptotic_counts.values()), max(necrotic_counts.values()))

# normalized_alive = {key: value / max_count for key, value in alive_counts.items()}
# normalized_apoptotic = {key: value / max_count for key, value in apoptotic_counts.items()}
# normalized_necrotic = {key: value / max_count for key, value in necrotic_counts.items()}

# plt.figure()
# plt.plot(normalized_alive.keys(), normalized_alive.values(), label='Alive')
# plt.plot(normalized_apoptotic.keys(), normalized_apoptotic.values(), label='Apoptotic')
# plt.plot(normalized_necrotic.keys(), normalized_necrotic.values(), label='Necrotic')


# plt.xlabel('Index')
# plt.ylabel('Normalized Cell Count')
# plt.legend()
# plt.savefig("normalized_alive_dead.png")
# plt.clf()