#!/bin/bash
#
#SBATCH --mail-user=<email>@ucr.ac.cr
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --job-name=demo-gpu
#SBATCH --output=demo-gpu.out
#
#SBATCH --nodes=1
#SBATCH --mem=1gb
#SBATCH --partition=gpu-long
#SBATCH --gres=gpu:1

module load miniconda3 cuda11.4
conda activate pydemo
srun python gpu_demo.py
