#!/bin/bash
export ROOT_DIR=``
export SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="${PYTHONPATH}:${SCRIPTPATH}/../src:${SCRIPTPATH}/../test"
echo $PYTHONPATH
#python -m apps.subscribe_and_write
python -m $*
