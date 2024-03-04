
##  Description
This repository contains scripts to control the iCub-simulator.
It covers on the one hand scripts to start the simulator environment with different options.
On the other hand there are python scripts to control the iCub and the environment in the simulator.


## Folder structure
- iCub_simulator_tools  -> main repository folder
    - iCubSim_environment   -> scripts, ini- and config-files for the iCub-simulator environment
        - cartesian -> config files for the cartesian controller; from [icub-main][icubmain] repository
        - data      -> model and textures from the iCub simulator
            - model/models  -> iCub models of the iCub-simulator; from [icub-main][icubmain] repository
            - texture       -> contains the textures for the iCub-simulator
                - skybox                -> active skybox textures (normal skybox textures); from [icub-main][icubmain] repository
                - skybox_black_white    -> black and white skybox textures; adapted normal skybox
                - skybox_black          -> black box; adapted normal skybox
                - skybox_sky            -> only sky as skybox textures; adapted normal skybox

        - *.ini files   -> ini files for the iCub simulator
        - *.xml files   -> config files for the iCub simulator
        - eye_ini       -> contains ini-files for the cameras
        - joint_ini     -> contains ini-files for the joints
        - sim_ini       -> contains ini-files for the simulator
        - Note: ini/xml files from [icub-main][icubmain] repository

        - new_models
            - bear  -> models and textures for the bear model
            - car   -> models and textures for the car model
            - cup   -> models and textures for the cup model
            - pen   -> models and textures for the pen model

        - start_cartesian_control.sh        -> start the necessary modules for the cartesian controller, including the simulator (right arm)
        - start_cartesian_control_modules.sh        -> start the necessary modules for the cartesian controller, give right_arm/left_arm as arguments to establish the use of the right/left arm or both arms e.g. "bash start_cartesian_control_modules right_arm left_arm"
        - start_environment.sh              -> start the iCub-simulator with two viewers for the eye cameras
        - start_simulator.sh                -> start only the iCub-simulator
        - start_skin_gui_right_arm.sh       -> start the skin gui for the right arm; the simulator has to be started first
        - start_skin_gui_right_forearm.sh   -> start the skin gui for the right forearm; the simulator has to be started first
        - start_skin_gui_right_hand.sh      -> start the skin gui for the right hand; the simulator has to be started first

    - gazebo_environment
        - gazebo_config
            - test_arm          -> experimental seperation of the right arm
            - worldInterface    -> contains the ini file for the gazebo worldinterface plugin
            - worlds            -> contains several predefined worlds for gazebo; partly taken from the [icub-gazebo][icubgazebo] repository
        - object_models
            - bear      -> contains sdf and model config file for the bear model
            - car       -> contains sdf and model config file for the car model
            - cup       -> contains sdf and model config file for the cup model
            - pen       -> contains sdf and model config file for the pen model
            - meshes    -> contains the meshes and the textures for all the models

        - start_cartesian_controller.sh -> start the necessary modules for the cartesian controller; the simulator has to be started first
        - start_environment.sh          -> start the gazebo-simulator with two viewers for the eye cameras and a predefined world

    - python_scripts -> contains python script for the work with the iCub/iCub-simulator
        - Python_libraries -> see [ReadMe](https://ai.informatik.tu-chemnitz.de/gogs/iCub_TUC/iCub_Python_Lib/src/master/ReadMe.md) for documentation
            - since this is a git submodule, execute the init_icubpylib.sh for initialization once
            - to update the submodule to the up-to-date version use the "git supdate" command

        - example_joint_cartesian_control.py    -> example for the joint control of the iCub, cartesian control(position in space)
        - example_joint_position_control.py     -> example for the joint control of the iCub, postion control(joint angles)
        - example_parameter_joint_control.py    -> parameter for the joint control example, e.g. transformationmatrix from simulator world reference frame to robot reference frame
        - gazebo_world_controller.py            -> control the gazebo-simulator environment, e.g. import objects

    - useful_links_iCub_YARP -> contains a collection of links, regarding different topics around the iCub ecosphere
    - init_icubpylib.sh -> initialize the iCub_Python_Lib submodule for the python examples (execute in your local clone of this repository)
    - add_icubpylib.sh -> add the iCub_Python_Lib submodule to your own project repository (copy and execute in your project repository)

## Hints
- Cartesian Controller:
    - Change the xml-file in yarprobotinterface.ini to configure the cartesian controller dependent on the selected xml-file.
    -> all: controller for arms and legs
    -> no_legs: controller only for arms

- The [HowToStart](./HowToStart.md) explain the installation process on Linux.
- See the documents in [iCub_control_system](./iCub_control_system) for more information about how to control the iCub
- The start_... scripts use xterm to seperately start the different tools. In case of errors with these scripts make sure that xterm is installed (sudo apt install xterm)


## Useful links
Wiki for the iCub robot: [http://wiki.icub.org/wiki/Manual](http://wiki.icub.org/wiki/Manual)

YARP website: [http://www.yarp.it/index.html](http://www.yarp.it/index.html)

for more see [useful_links_iCub_YARP](./useful_links_iCub_YARP)


## Authors
Torsten Fietzek<br>
config files (.ini, .xml, .world, etc.) from [icub-main][icubmain] and [icub-gazebo][icubgazebo] repositories<br>
if based on work of others, they are named in the files


## Dependencies
- Software:
    - Python  >= 3.5
    - YARP    >= 3.2 (with Python-bindings)
    - OpenCV  >= 3.4
    - SWIG    >= 3.0.12
    - xterm

    - iCub-simulator      >=
        or gazebo-simulator == 9.0 or 10.0

- Python Packages:
    - numpy
    - matplotlib.pylab
    - OpenCV



[icubmain]: https://github.com/robotology/icub-main
[icubgazebo]: https://github.com/robotology/icub-gazebo
