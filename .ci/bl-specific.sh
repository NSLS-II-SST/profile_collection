#!/bin/bash

conda install -y -c ${CONDA_CHANNEL_NAME} \
    ansiwrap \
    "ophyd>=1.4.0rc5" \
    bluesky-darkframes \
    "pyepics>=3.4.1"
