# BIRDMAn Example Code

Here I've included a framework for running [BIRDMAn](https://www.biorxiv.org/content/10.1101/2023.01.30.526328v1) on a SLURM server. 

**1) Install BIRDMAn.**
If you have trouble with installation [here](https://birdman.readthedocs.io/en/stable/?badge=stable), feel free to use the .yml file that I've provided in the repo: 

`conda env create -f birdman.yml`

**2) Clone this repo.**

`git clone https://github.com/ahdilmore/MARS_Birdman.git`

**3) Create your model.** Templates are provided in [birdman/src/model_amyloid_single.py](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/src/model_amyloid_single.py) 
and [birdman/src/model_apoe4_single.py](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/src/model_apoe4_single.py). 

**4) Modify chunking file.** Templates are provided in [birdman/src/amyloid_birdman_chunked.py](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/src/amyloid_birdman_chunked.py)
and [birdman/src/apoe4_birdman_chunked.py](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/src/apoe4_birdman_chunked.py)

**4) Modify overall script, then run it.** Templates are provided in [birdman/amyloid/zebra.sh](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/amyloid/zebra.sh)
and [birdman/apoe4/zebra.sh](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/apoe4/zebra.sh). 
You will know that the script is complete when (1) SLURM emails you or (2) .nc files are created in your inferences directory for each feature. 

`sbatch zebra.sh`

**5) Modify path in [summarize-inferences](birdman/amyloid/summarize-inferences.sh), then run it.**
You will know that the script is complete when (1) SLURM emails you or (2) You have a .tsv file in your inferences-results directory. 

`sbatch summarize-inferences.sh`

**6) Import the .tsv files into the [analysis notebook](https://github.com/ahdilmore/MARS_Birdman/blob/8084f938a606babe75f42fbe9274da7a431c90ae/birdman/zebra_birdman_analysis.ipynb) to analyze results.**
