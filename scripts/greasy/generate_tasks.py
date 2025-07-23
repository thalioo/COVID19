with open("tasks_complete.txt", 'w') as file:
        for i in range(1, 1801):
            file.write(f"python3 getcsv.py \"/gpfs/scratch/bsc08/bsc008602/vm_emews_pbc/experiments/new_deposition_correct/instance_{i}\"\n")
