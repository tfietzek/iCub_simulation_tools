
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path
TOOLDIR=$(realpath "$0" | sed 's|\(.*\)/.*/.*|\1|') # -> Simtools path

cpath=$(which conda)
conda_path="${cpath%/*/*}"



. ~/.bashrc

conda config --set auto_activate false

conda info


if [ $# == 0 ]
then
    env_name="iCub"
else
    env_name=$1
fi
conda create -n ${env_name} -y
conda install -n ${env_name} -c conda-forge -c robotology yarp icub-main gz-sim-yarp-plugins icub-models -y

echo "Set env variables in bashrc"
cp ~/.bashrc $BASEDIR/.bashrc_prep_bak_$(date  "+%Y_%m_%d_%H_%M_%S")

# Set environment variables for iCub and Gezeob Ressources (Models, Plugins, Worlds, ...) #

ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
ICUB_TOOLDIR="$TOOLDIR"

# iCub stuff for YARP and gazebo
conda env config vars set -n ${env_name} "YARP_DATA_DIRS=$ICUB_INSTALL_PREFIX/share/yarp:$ICUB_INSTALL_PREFIX/share/iCub"
conda env config vars set -n ${env_name} "GZ_SIM_RESOURCE_PATH=$ICUB_INSTALL_PREFIX/lib:$ICUB_INSTALL_PREFIX/share/gazebo/models:$ICUB_INSTALL_PREFIX/share/iCub/robots:$ICUB_INSTALL_PREFIX/share:$ICUB_TOOLDIR/gz_env/object_models:$ICUB_TOOLDIR/gz_env/gazebo_config/worlds"


# Add alias to .bashrc to activate environment easily 
rcadditions="alias ${env_name}='conda activate ${env_name}'
"

rcFile=~/.bashrc
echo -e "$rcadditions" >> $rcFile


echo "Finished"
