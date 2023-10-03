#!/bin/bash
#
# clean up any old builds
#
rm -Rf build/
#
# build conda package
#
conda run -n mamba-build conda mambabuild --python=3.10 --no-remove-work-dir packaging/conda --output-folder build
