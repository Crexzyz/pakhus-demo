#!/bin/bash
#
#SBATCH --mail-user=<email>@ucr.ac.cr
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --job-name=demo-cpu
#SBATCH --output=demo-cpu.out
#
#SBATCH --nodes=1
#SBATCH --mem=1gb
#SBATCH --partition=cpu-only

module load miniconda3
conda activate pydemo
srun python gpu_demo.py
