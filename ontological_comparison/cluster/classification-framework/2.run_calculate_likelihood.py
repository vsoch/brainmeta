#!/usr/bin/python
from glob import glob
import os

base = "/share/PI/russpold/work/IMAGE_COMPARISON/ONTOLOGICAL_COMPARISON"
data = "%s/data" %base        # mostly images
priors_pickles = glob("%s/likelihood/*.pkl" %(data))
tables_folder = "%s/likelihood/tables" %(data) # output folder for likelihood tables

if not os.path.exists(tables_folder):
    os.mkdir(tables_folder)

for p in range(1,len(priors_pickles)):
    pkl = priors_pickles[p]
    contrast_id = os.path.split(pkl)[-1].split("_")[-1].replace(".pkl","")
    filey = ".jobs/revinf_%s.job" %(contrast_id)
    filey = open(filey,"w")
    filey.writelines("#!/bin/bash\n")
    filey.writelines("#SBATCH --job-name=%s\n" %(contrast_id))
    filey.writelines("#SBATCH --output=.out/%s.out\n" %(contrast_id))
    filey.writelines("#SBATCH --error=.out/%s.err\n" %(contrast_id))
    filey.writelines("#SBATCH --time=2-00:00\n")
    filey.writelines("#SBATCH --mem=64000\n")
    filey.writelines("python /home/vsochat/SCRIPT/python/brainmeta/ontological_comparison/cluster/2.calculate_likelihood.py %s %s" %(pkl, tables_folder))
    filey.close()
    os.system("sbatch -p russpold " + ".jobs/revinf_%s.job" %(contrast_id)) 
