#!/bin/bash

export RE_METADATA="/areadata/rsoxs-collection/runengine-metadata"

sudo mkdir -v -p ${RE_METADATA}
sudo chown -Rv $USER: ${RE_METADATA}

python3 .ci/gen-metadata.py
