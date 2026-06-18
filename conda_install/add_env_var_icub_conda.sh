
#!usr/bin/env bash -i
BASEDIR=$(realpath "$0" | sed 's|\(.*\)/.*|\1|') # -> script path
TOOLDIR=$(realpath "$0" | sed 's|\(.*\)/.*/.*|\1|') # -> Simtools path

cpath=$(which conda)
conda_path="${cpath%/*/*}"



# . ~/.bashrc


if [ $# == 0 ]
then
    env_name="iCub" 
else
    env_name=$1
fi

ICUB_INSTALL_PREFIX="$conda_path"/envs/"$env_name"
ICUB_TOOLDIR="$TOOLDIR"

# Official iCub stuff for gazebo
conda env config vars set -n ${env_name} "YARP_DATA_DIRS=$ICUB_INSTALL_PREFIX/share/yarp:$ICUB_INSTALL_PREFIX/share/iCub"
conda env config vars set -n ${env_name} "GAZEBO_PLUGIN_PATH=${ICUB_INSTALL_PREFIX}/lib"
conda env config vars set -n ${env_name} "GAZEBO_RESOURCE_PATH=${ICUB_INSTALL_PREFIX}/share/gazebo-11/worlds:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worlds:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worldinterface"
conda env config vars set -n ${env_name} "GAZEBO_MODEL_PATH=${ICUB_INSTALL_PREFIX}/share/gazebo/models:${ICUB_INSTALL_PREFIX}/share/iCub/robots:${ICUB_INSTALL_PREFIX}/share:${ICUB_TOOLDIR}/gazebo_environment/object_models:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worlds:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config/worldinterface:${ICUB_TOOLDIR}/gazebo_environment/gazebo_config"
