#!/bin/bash
#
# clean up any old builds
#
rm -Rf build/
#
# build conda package
#
# chose the target environement: needs conda-build, setuptools and boa (for mambabuild)
#
conda run -n mamba-build2 conda mambabuild --python=3.11 --no-remove-work-dir packaging/conda --output-folder build
#
#