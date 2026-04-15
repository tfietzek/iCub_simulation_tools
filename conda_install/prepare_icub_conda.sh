
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
    postfix=""
else
    env_name=$1
    postfix="_${env_name}"
fi

conda create -y -n ${env_name} python==3.9
conda install -y -n ${env_name} -c robotology opencv yarp==3.8.1 icub-main gazebo-yarp-plugins icub-models


if [ -z "${ICUB_INSTALL_PREFIX}" ] || [ "${ICUB_INSTALL_PREFIX}" != "${conda_path}/envs/${env_name}" ];
then
echo "Set official iCub/YARP env variables in bashrc"
cp ~/.bashrc $BASEDIR/.bashrc_prep_bak_$(date  "+%Y_%m_%d_%H_%M_%S")

rcadditions="""
alias iCub${postfix}='conda activate ${env_name}'
export ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
"""

rcadditions1='''
# Env Variables for iCub/YARP/Gazebo (official packages)
source $ICUB_INSTALL_PREFIX/share/gazebo/setup.sh
export YARP_DATA_DIRS=${YARP_DATA_DIRS:+${YARP_DATA_DIRS}:}$ICUB_INSTALL_PREFIX/share/yarp:$ICUB_INSTALL_PREFIX/share/iCub
export GAZEBO_PLUGIN_PATH=${GAZEBO_PLUGIN_PATH:+${GAZEBO_PLUGIN_PATH}:}${ICUB_INSTALL_PREFIX}/lib
export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH:+${GAZEBO_RESOURCE_PATH}:}${ICUB_INSTALL_PREFIX}/share/gazebo-11/worlds
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH:+${GAZEBO_MODEL_PATH}:}${ICUB_INSTALL_PREFIX}/share/gazebo/models:${ICUB_INSTALL_PREFIX}/share/iCub/robots:${ICUB_INSTALL_PREFIX}/share

'''

rcFile=~/.bashrc

echo -e "$rcadditions$rcadditions1" >> $rcFile

fi


if [ -z "${ICUB_TOOLDIR}" ] || [ "${ICUB_TOOLDIR}" != "${TOOLDIR}" ];
then
echo "Set model env variables in bashrc"
cp ~/.bashrc $BASEDIR/.bashrc_prep_bak_$(date  "+%Y_%m_%d_%H_%M_%S")

rcadditions="""
export ICUB_TOOLDIR="$TOOLDIR"
"""

rcadditions1='''
# individual models/worlds for Gazebo (Classic)
export GAZEBO_MODEL_PATH=${GAZEBO_MODEL_PATH}:${ICUB_TOOLDIR}/gazebo_environment/object_models
export GAZEBO_RESOURCE_PATH=${GAZEBO_RESOURCE_PATH}:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worlds

'''

rcFile=~/.bashrc

echo -e "$rcadditions$rcadditions1" >> $rcFile

fi