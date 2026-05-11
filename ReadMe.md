## Description

This repository contains scripts to control the iCub-simulator.
It covers on the one hand scripts to start the simulator environment with different options.
On the other hand there are python scripts to control the iCub and the environment in the simulator.

## Folder structure

- __iCub_simulation_tools__ -> main repository folder
  - __conda_install__ -> scripts to setup conda and a conda environment with the iCub software installed, including the related environment variables
    - *install_conda.sh* -> download miniforge and install conda
    - *prepare_icub_conda.sh* -> conda environment with classic gazebo
    - *{experimental} prepare_icub_conda_gz.sh* -> conda environment with modern gazebo
  - __{Deprecated} iCubSim_environment__ -> scripts, ini- and config-files for the iCub-simulator environment
    - __cartesian__ -> config files for the cartesian controller; from [icub-main][icubmain] repository
    - __data__ -> model and textures from the iCub simulator
      - __model/models__ -> iCub models of the iCub-simulator; from [icub-main][icubmain] repository
      - __texture__ -> contains the textures for the iCub-simulator
        - __skybox__ -> active skybox textures (normal skybox textures); from [icub-main][icubmain] repository
        - __skybox_black_white__ -> black and white skybox textures; adapted normal skybox
        - __skybox_black__ -> black box; adapted normal skybox
        - __skybox_sky__ -> only sky as skybox textures; adapted normal skybox

    - *\*.ini files* -> ini files for the iCub simulator
    - *\*.xml files* -> config files for the iCub simulator
    - __eye_ini__ -> contains ini-files for the cameras
    - __joint_ini__ -> contains ini-files for the joints
    - __sim_ini__ -> contains ini-files for the simulator
    *Note*: ini/xml files from [icub-main][icubmain] repository

    - __new_models__
      - __bear__ -> models and textures for the bear model
      - __car__ -> models and textures for the car model
      - __cup__ -> models and textures for the cup model
      - __pen__ -> models and textures for the pen model

    - *start_cartesian_control.sh* -> start the necessary modules for the cartesian controller, including the simulator (right arm)
    - *start_cartesian_control_modules.sh* -> start the necessary modules for the cartesian controller, give right_arm/left_arm as arguments to establish the use of the right/left arm or both arms e.g. "bash start_cartesian_control_modules right_arm left_arm"
    - *start_environment.sh* -> start the iCub-simulator with two viewers for the eye cameras
    - *start_simulator.sh* -> start only the iCub-simulator
    - *start_skin_gui_right_arm.sh* -> start the skin gui for the right arm; the simulator has to be started first
    - *start_skin_gui_right_forearm.sh* -> start the skin gui for the right forearm; the simulator has to be started first
    - *start_skin_gui_right_hand.sh* -> start the skin gui for the right hand; the simulator has to be started first

  - __gazebo_environment__ -> scripts and files for classic gazebo
    - __gazebo_config__
      - __test_arm__ -> experimental seperation of the right arm
      - __worldInterface__ -> contains the ini file for the gazebo worldinterface plugin
      - __worlds__ -> contains several predefined worlds for gazebo; partly taken from the [icub-gazebo][icubgazebo] repository
    - __object_models__
      - __bear__ -> contains sdf and model config file for the bear model
      - __car__ -> contains sdf and model config file for the car model
      - __cup__ -> contains sdf and model config file for the cup model
      - __pen__ -> contains sdf and model config file for the pen model
      - __meshes__ -> contains the meshes and the textures for all the models
    - *start_simulator.sh (world_filename)* -> start yarpserver and modern gazebo simulator with the iCub (optional receives name of a sdf-world file)
    - *start_simulator_no_gui.sh (world_filename)* -> start yarpserver and simulator; the simulator is started without a GUI-client
    - *start_simulator_no_gui_screen.sh (world_filename)* -> start yarpserver and simulator in screen sessions; the simulator is started without a GUI-client
    - *start_environment.sh (world_filename)* -> start the gazebo-simulator with two viewers for the eye cameras and a predefined world
    - *start_viewer.sh* -> start two viewers for the eye cameras
    - *connect_viewer.sh* -> connect two viewers for the eye camera to the robot
    - *start_cartesian_controller.sh {right/left}\_arm* -> start the necessary modules for the cartesian controller; the simulator has to be started first

  - __gz_environment__ -> scripts and files for modern gazebo
    - __gazebo_config__
      - __worlds__ -> contains predefined worlds for modern gazebo
    - *start_simulator.sh (world_filename)* -> start yarpserver and modern gazebo simulator with the iCub (optional receives name of a sdf-world file)
    - *start_simulator_no_gui.sh (world_filename)* -> start yarpserver and simulator; the simulator is started without a GUI-client
    - *start_simulator_no_gui_screen.sh (world_filename)* -> start yarpserver and simulator in screen sessions; the simulator is started without a GUI-client
    - *start_environment.sh (world_filename)* -> start the gazebo-simulator with two viewers for the eye cameras and a predefined world
    - *start_viewer.sh* -> start two viewers for the eye cameras
    - *connect_viewer.sh* -> connect two viewers for the eye camera to the robot
    - *start_cartesian_controller.sh {right/left}\_arm* -> start the necessary modules for the cartesian controller; the simulator has to be started first

  - __python_scripts__ -> contains python script for the work with the iCub/iCub-simulator
    - __Python_libraries__ -> see [ReadMe](https://github.com/tfietzek/iCub_Python_Lib/blob/master/ReadMe.md) for documentation
      - since this is a git submodule, execute the init_icubpylib.sh for initialization once
      - to update the submodule to the up-to-date version use the "git supdate" command

    - *example_joint_cartesian_control.py* -> example for the joint control of the iCub, cartesian control(position in space)
    - *example_joint_position_control.py* -> example for the joint control of the iCub, postion control(joint angles)
    - *example_joint_forward_kinematics.py* -> iCub forward kinematic
    - *example_joint_inverse_kinematics.py* -> iCub inverse kinematic
    - *example_visual_perception.py* -> iCub camera
    - *example_scene_control.py* -> object/model crontrol for iCubSim and gazebo classic
    - *example_scene_video.py* -> video of the robot in the virtual environment (iCubSim and gazebo classic)
    - *example_parameter_joint_control.py* -> parameter for the joint control example, e.g. transformationmatrix from simulator world reference frame to robot reference frame
    - *gazebo_world_controller.py* -> control the gazebo-classic environment, e.g. import objects

  - *useful_links_iCub_YARP* -> contains a collection of links, regarding different topics around the iCub ecosphere
  - *init_icubpylib.sh* -> initialize the iCub_Python_Lib submodule for the python examples (execute in your local clone of this repository)
  - *add_icubpylib.sh* -> add the iCub_Python_Lib submodule to your own project repository (copy and execute in your project repository)

## Hints

- Cartesian Controller:
  - Change the xml-file in yarprobotinterface.ini to configure the cartesian controller dependent on the selected xml-file.
    -> all: controller for arms and legs
    -> no_legs: controller only for arms

- See the documents in [iCub_control_system](./iCub_control_system) for more information about how to control the iCub
- The start\_... scripts use xterm to seperately start the different tools. In case of errors with these scripts make sure that xterm is installed (sudo apt install xterm)

## Useful links

see [useful_links_iCub_YARP](./useful_links_iCub_YARP)

## Authors

Torsten Fietzek<br>
config files (.ini, .xml, .world, etc.) from [icub-main][icubmain] and [icub-gazebo][icubgazebo] repositories<br>
if based on work of others, they are named in the files

## Dependencies

- Software:
  - Python >= 3.9
  - YARP >= 3.6 (with Python-bindings)
  - OpenCV >= 3.4
  - SWIG >= 3.0.12
  - xterm

  - iCub-simulator
  - gazebo classic == 11.0
  - modern gazebo >= 8.10

- Python Packages:
  - numpy
  - matplotlib.pylab
  - OpenCV

[icubmain]: https://github.com/robotology/icub-main
[icubgazebo]: https://github.com/robotology/icub-gazebo
