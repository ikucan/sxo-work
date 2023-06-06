#!/bin/bash
echo "running the mainline script"

mamba run -n sxo --no-capture-output python /scratch/run.py
