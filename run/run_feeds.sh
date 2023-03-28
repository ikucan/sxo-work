#!/bin/bash
export ROOT_DIR=``
export SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
export PYTHONPATH="${PYTHONPATH}:${SCRIPTPATH}/../src:${SCRIPTPATH}/../test"
echo $PYTHONPATH
#
#
export TOKEN_FILE=/tmp/saxo_token
export DATA_DIR=/data
export INSTRUMENTS=GBPEUR
#
#
python ../src/apps/data_capture.py
