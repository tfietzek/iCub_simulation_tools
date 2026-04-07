#!/bin/bash
echo "Script executed from: ${PWD}"

# $(dirname $0) -> script path

BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') 

# $BASEDIR/miniforge/condabin/conda init --reverse
# $BASEDIR/miniforge/condabin/mamba init --reverse

# Use this first command to see what rc files will be updated
conda init --reverse --dry-run
# Use this next command to take action on the rc files listed above
conda init --reverse
# Temporarily IGNORE the shell message
#       'For changes to take effect, close and re-open your current shell.',
# and CLOSE THE SHELL ONLY AFTER the 3rd step below is completed.

CONDA_BASE_ENVIRONMENT="$(conda info --base)"
echo The next command will delete all files in "${CONDA_BASE_ENVIRONMENT}"
# Warning, the rm command below is irreversible!
# check the output of the echo command above
# To make sure you are deleting the correct directory
rm -rf "${CONDA_BASE_ENVIRONMENT}"

echo ${HOME}/.condarc will be removed if it exists
rm -f "${HOME}/.condarc"
echo ${HOME}/.conda and underlying files will be removed if they exist.
rm -fr "${HOME}/.conda"

rm -f Miniforge3-$(uname)-$(uname -m).sh

# remove iCub related environment variables from bashrc
cp ~/.bashrc $BASEDIR/.bashrc_remove_bak_$(date  "+%Y_%m_%d_%H_%M_%S")
var=$(cat ~/.bashrc | grep -Pvi "ICUB_INSTALL_PREFIX|# Env Variables for iCub/YARP/Gazebo|alias iCub.*='conda activate|# individual models/worlds for Gazebo|ICUB_TOOLDIR")
echo -e "$var" > ~/.bashrc
