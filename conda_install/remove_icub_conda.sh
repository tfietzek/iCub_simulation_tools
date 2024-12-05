#!/bin/bash
echo "Script executed from: ${PWD}"

# $(dirname $0) -> script path

BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') 

$BASEDIR/miniforge/condabin/conda init --reverse
$BASEDIR/miniforge/condabin/mamba init --reverse

rm -f Miniforge3-$(uname)-$(uname -m).sh
rm -rf $BASEDIR/miniforge
rm -rf ~/.conda
rm -rf ~/.condarc

cp ~/.bashrc $BASEDIR/.bashrc_remove_bak
var=$(cat ~/.bashrc | grep -Pvi "ICUB_INSTALL_PREFIX|# Env Variables for iCub/YARP/Gazebo|alias='mamba activate iCub")
echo -e "$var" > ~/.bashrc
