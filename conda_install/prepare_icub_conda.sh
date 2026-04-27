
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path
TOOLDIR=$(realpath "$0" | sed 's|\(.*\)/.*/.*|\1|') # -> Simtools path

cpath=$(which conda)
conda_path="${cpath%/*/*}"



# . ~/.bashrc

conda config --set auto_activate false

conda info

if [ $# == 0 ]
then
    env_name="iCub" 
else
    env_name=$1
fi

conda create -y -n ${env_name} python==3.11
conda install -y -n ${env_name} -c robotology opencv yarp icub-main gazebo-yarp-plugins icub-models


if [ -z "${ICUB_INSTALL_PREFIX}" ] || [ "${ICUB_INSTALL_PREFIX}" != "${conda_path}/envs/${env_name}" ];
then
echo "Set official iCub/YARP env variables in bashrc"
cp ~/.bashrc $BASEDIR/.bashrc_prep_bak_$(date  "+%Y_%m_%d_%H_%M_%S")

conda env config vars set -n ${env_name} ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
conda env config vars set -n ${env_name} ICUB_INSTALL_PREFIX="ICUB_TOOLDIR="$TOOLDIR""

# Official iCub stuff for gazebo
conda env config vars set -n ${env_name} "YARP_DATA_DIRS=\${YARP_DATA_DIRS}:\$ICUB_INSTALL_PREFIX/share/yarp:\$ICUB_INSTALL_PREFIX/share/iCub"
conda env config vars set -n ${env_name} "GAZEBO_PLUGIN_PATH=\${GAZEBO_PLUGIN_PATH:+\${GAZEBO_PLUGIN_PATH}:}\${ICUB_INSTALL_PREFIX}/lib"
conda env config vars set -n ${env_name} "GAZEBO_RESOURCE_PATH=\${GAZEBO_RESOURCE_PATH:+\${GAZEBO_RESOURCE_PATH}:}\${ICUB_INSTALL_PREFIX}/share/gazebo-11/worlds"
conda env config vars set -n ${env_name} "GAZEBO_MODEL_PATH=\${GAZEBO_MODEL_PATH:+\${GAZEBO_MODEL_PATH}:}\${ICUB_INSTALL_PREFIX}/share/gazebo/models:\${ICUB_INSTALL_PREFIX}/share/iCub/robots:\${ICUB_INSTALL_PREFIX}/share"

# Individual iCub stuff for gazebo
conda env config vars set -n ${env_name} "GAZEBO_MODEL_PATH=\${GAZEBO_MODEL_PATH}:\${ICUB_TOOLDIR}/gazebo_environment/object_models"
conda env config vars set -n ${env_name} "GAZEBO_RESOURCE_PATH=\${GAZEBO_RESOURCE_PATH}:\${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worlds"


rcadditions="""
alias ${env_name}='conda activate ${env_name}'
export ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
source $ICUB_INSTALL_PREFIX/share/gazebo/setup.sh

"""

rcFile=~/.bashrc

echo -e "$rcadditions" >> $rcFile

fi
