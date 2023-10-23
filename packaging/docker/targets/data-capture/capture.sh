#!/bin/bash
echo "running the mainline script"

source ~/.bashrc && mamba run -n sxo --no-capture-output python /scratch/capture.py
