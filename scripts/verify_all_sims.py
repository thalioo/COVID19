# looks in each instance folder to see  if the simmulation finished.
import glob
output_folder = "/home/tntiniak/Work/mnt/experiments/new_deposition_correct/"
# for each folder that starts with instance_ and ends with a number

for folder in glob.glob(output_folder + "/instance_*/output/"):
    print(folder)
    # check if there is a file called "finished"
    if not glob.glob(folder + "output0000000410.xml"):
        print("Simulation not finished in", folder)
    else: 
        continue