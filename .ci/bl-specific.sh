#!/bin/bash

sudo mkdir -v -p /areadata/rsoxs-collection/runengine-metadata
sudo chown -Rv $USER: /areadata/rsoxs-collection/runengine-metadata

cp -v .ci/fake-metadata/* /areadata/rsoxs-collection/runengine-metadata/
