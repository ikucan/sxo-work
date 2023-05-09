#!/bin/bash
#
# clean up any old builds
#
rm -Rf build/
#
# build conda package
#
conda run -n mamba-build conda mambabuild --python=3.10 --no-remove-work-dir packaging/conda --output-folder build
#
# copy the binary and the repo information to target directory
#
export TARGET_DOCKER_DIR=packaging/docker/targets/data-feeds/
#
rm -f $TARGET_DOCKER_DIR/ik.sxo-v0.1.0-py311_0.tar.bz2
rm -f $TARGET_DOCKER_DIR/repodata-linux-64.json
rm -f $TARGET_DOCKER_DIR/repodata-noarch.json
#
cp build/linux-64/ik.sxo-v0.1.0-py311_0.tar.bz2 $TARGET_DOCKER_DIR
cp build/linux-64/repodata.json $TARGET_DOCKER_DIR/repodata-linux-64.json
cp build/noarch/repodata.json $TARGET_DOCKER_DIR/repodata-noarch.json
#
# kick off the docker build
#
cd $TARGET_DOCKER_DIR && make
