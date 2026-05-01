# Pakhus Demo

This repository contains a set of demo Python projects to run under the Slurm workload manager at Pakhus from the University of Costa Rica

# Prerequisites

1. Access to the ECCI VPN
1. An account at the Pakhus cluster
1. A terminal with `ssh`
1. For local development, a recent Python installation

# Folders

1. [configs](./configs/): Contains some configurations to make the terminal-only environment at Pakhus more beginne-friendly. With `tmux` configurations for mouse integration, intuitive shortcuts and `vim` configurations that makes it feel more similar to IDEs or text editors.
1. [src](./src): contains some Python projects that can run in the cluster as an example of how to use the CPU and GPU queues. Check the folder for more information

# Quick command reference

1. `scontrol show jobs`: see current running and in queue jobs
1. `sinfo`: see available queues
1. `scontrol show partitions`: detailed information about each queue
1. `sbatch <bash file>`: add a run into the queue
1. `scancel <id>`: cancel a run with a specific ID

# Other links

Helpful cheatsheets:
1. `tmux`: https://tmuxcheatsheet.com/
1. `vim`: https://vim.rtorr.com/
1. Slurm: https://slurm.schedmd.com/pdfs/summary.pdf