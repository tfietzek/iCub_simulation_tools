
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path

cpath=$(which conda)
conda_path="${cpath%/*/*}"



. ~/.bashrc

conda config --set auto_activate_base false

conda info
conda deactivate


if [ $# == 0 ]
then
    env_name="iCub" 
else
    env_name=$1
fi
mamba create -n ${env_name}
mamba activate ${env_name}

mamba install -n ${env_name} -c robotology -y opencv yarp icub-main gazebo-yarp-plugins icub-models

if [ -z "${ICUB_INSTALL_PREFIX}" ] || [ "${ICUB_INSTALL_PREFIX}" != "${conda_path}/envs/robotologyenv" ];
then
echo "Set env variables in bashrc"
cp ~/.bashrc $BASEDIR/.bashrc_prep_bak

rcadditions="""
alias iCub='mamba activate ${env_name}'
export ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
"""

rcadditions1='''
# Env Variables for iCub/YARP/Gazebo
source $ICUB_INSTALL_PREFIX/share/gazebo/setup.sh
export YARP_DATA_DIRS=${YARP_DATA_DIRS:+${YARP_DATA_DIRS}:}$ICUB_INSTALL_PREFIX/share/yarp:$ICUB_INSTALL_PREFIX/share/iCub
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH:+${GAZEBO_PLUGIN_PATH}:}${ICUB_INSTALL_PREFIX}/lib
export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH:+${GAZEBO_RESOURCE_PATH}:}${ICUB_INSTALL_PREFIX}/share/gazebo-11/worlds
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH:+${GAZEBO_MODEL_PATH}:}${ICUB_INSTALL_PREFIX}/share/gazebo/models:${ICUB_INSTALL_PREFIX}/share/iCub/robots:${ICUB_INSTALL_PREFIX}/share
'''

rcFile=~/.bashrc

echo -e "$rcadditions$rcadditions1" >> $rcFile

fi
