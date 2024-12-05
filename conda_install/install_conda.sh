
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path

Download
curl -LO https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh

Install with default options
sh Miniforge3-$(uname)-$(uname -m).sh -b -p $BASEDIR/miniforge

$(dirname "$0")/miniforge/condabin/conda init
$(dirname "$0")/miniforge/condabin/mamba init
