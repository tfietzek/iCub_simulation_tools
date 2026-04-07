
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path

# Download
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

# Install with default options
bash Miniforge3-$(uname)-$(uname -m).sh -b -p $BASEDIR/miniforge

$(dirname "$0")/miniforge/bin/conda init bash

