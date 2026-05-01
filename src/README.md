# Running the demo

This folder has the Python source and Slurm files needed to run a project in the Pakhus cluster

# Set up the Python environment

To run the CPU-GPU demo you will first need to set up the environment:

```bash
module load miniconda3
conda create -n pydemo python=3.12
conda activate pydemo
pip install -r requirements.txt
```

There are other Conda-native setup methods as well, feel free to use the one that fits your needs.

# Queue some runs

At the `demo-cpu.sh` and `demo-gpu.sh`, **remember to change** the `--mail-user` value to your own email. Then:

1. For the CPU example: `sbatch demo-cpu.sh`
1. For the GPU example: `sbatch demo-gpu.sh`

# Utility commands to monitor runs

1. Use `tmux` to keep your terminal session open even after a VPN timeout
    1. Split the terminal with `ctrl` + `a` and the `|` or `-` key
    1. Restore it with `tmux a`
1. Monitor the latest output of the run with
    ```bash
    watch -n 1 tail -n 10 gpu-demo.out
    ```