#!/bin/bash
#
#SBATCH --workdir=//scratch/lsanmartin/Peruvian-presidents-speeches/notebooks/data_preparation
#SBATCH --job-name=data_cleaning-speeches
#SBATCH --mail-user=lsanmartin@cs.uchicago.edu
#SBATCH --mail-type=ALL
#SBATCH --output=sbatch/2_data_preparation.out
#SBATCH --error=sbatch/2_data_preparation.err
#SBATCH --partition=general
#SBATCH --mem-per-cpu=10000
#SBATCH --nodes=1
#SBATCH --ntasks=1

pip3 install lxml --user
python3 2_data_preparation.py