#!/bin/bash
#
# build conda package 
#
conda run -n mamba-build conda mambabuild --python=3.10 --no-remove-work-dir packaging/conda --output-folder build
#
# copy the binary and the repo information to target directory
#
export TARGET_DOCKE_DIR=packaging/docker/targets/data-feeds/
#
cp build/linux-64/ik.sxo-v0.1.0-py311_0.tar.bz2 $TARGET_DOCKE_DIR
cp build/linux-64/repodata.json $TARGET_DOCKE_DIR/repodata-linux-64.json
cp build/noarch/repodata.json $TARGET_DOCKE_DIR/repodata-noarch.json
