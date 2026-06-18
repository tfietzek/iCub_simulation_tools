
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path

if (( ${#BASEDIR} > 103 ))
    then 
        echo "The path length exceeds the safe limit for conda of 103 characters. Please use a shorter path!"
        exit
fi
# if the path is above 103 characters, the python interpreter in miniforge/{conda}bin/conda is set to /usr/bin/env python instead of .../miniforge/bin/python


# Download
curl -L -O "https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-$(uname)-$(uname -m).sh"

# Install with default options
bash Miniforge3-$(uname)-$(uname -m).sh -b -p $BASEDIR/miniforge

$(dirname "$0")/miniforge/bin/conda init bash

