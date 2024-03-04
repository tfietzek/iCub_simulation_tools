"""
Created on Tue July 07 2020

@author: Torsten Fietzek

Visual perception example

"""

######################################################################
########################## Import modules  ###########################
######################################################################

import os
import sys
import time

import matplotlib.pylab as plt
import numpy as np
import yarp

################ Import parameter from parameter file ################
import example_parameter as params

############# Import control classes for both simulators #############
if params.GAZEBO_SIM:
    import Python_libraries.gazebo_world_controller as gzbo_ctrl
else:
    import Python_libraries.iCubSim_world_controller as iCubSim_ctrl
    import Python_libraries.iCubSim_model_groups_definition as mdl_define
    import Python_libraries.iCubSim_model_groups_control as mdl_ctrl


def objects_gzbo():
    gzbo_wrld_ctrl = gzbo_ctrl.WorldController()

    # create simple objects
    box_id = gzbo_wrld_ctrl.create_object("box", [0.1, 0.1, 0.1], [1, 0.25, 1.], [0, 0, 0], [1, 1, 1] )
    cyl_id = gzbo_wrld_ctrl.create_object("cylinder", [0.1, 0.1], [1, 0.5, 0.5], [0, 0, 0], [1, 1, 1] )
    sphere_id = gzbo_wrld_ctrl.create_object("sphere", [0.1], [1., 1., 1.], [0, 0, 0], [1, 1, 1] )

    gzbo_wrld_ctrl.set_pose(box_id, [1., 0.5, 2.], [1, 1, 1])
    print(gzbo_wrld_ctrl.get_list())

    for i in range(20):
        gzbo_wrld_ctrl.set_pose(box_id, [1 + i*0.1, 0.5, 2.], [1, 1, 1])
        time.sleep(1.)

    # create complex models
    # two ways:
    # 1. add the model path in the .bashrc to the GAZEBO_MODEL_PATH variable
    # car = gzbo_wrld_ctrl.create_model('/car/car.sdf', [0.5, 1, 0.5], [0, 0, 0])

    # 2. use full path to the model
    model_path = os.path.abspath("../gazebo_environment/object_models")
    car = gzbo_wrld_ctrl.create_model(model_path + '/car/car.sdf', [0.5, 1, 0.5], [0, 0, 0])

    del gzbo_wrld_ctrl

def objects_iCubSim():
    # create simple objects
    iCubSim_wrld_ctrl = iCubSim_ctrl.WorldController()

    box_id = iCubSim_wrld_ctrl.create_object("sbox", [0.1, 0.1, 0.1], [0.25, 0.5, 0.5], [1, 1, 1])
    cyl_id = iCubSim_wrld_ctrl.create_object("scyl", [0.1, 0.1], [0.5, 0.5, 0.3], [1, 1, 1])
    sphere_id = iCubSim_wrld_ctrl.create_object("ssph", [0.1], [-0.5, 0.5, 0.3], [1, 1, 1])
    time.sleep(4.)

    iCubSim_wrld_ctrl.move_object(box_id, [0.25, 1., 0.5])

    for i in range(10):
        iCubSim_wrld_ctrl.move_object(box_id, [0.25, 0.2 + i*0.1, 0.4])
        time.sleep(1.)

    iCubSim_wrld_ctrl.rotate_object(cyl_id, [0, 90, 0])
    time.sleep(4.)

    iCubSim_wrld_ctrl.del_all()

    # create complex models
    model_path = os.path.abspath("../iCubSim_environment/new_models")

    bear_dict = mdl_define.dictionary_bear
    bear = mdl_ctrl.ModelGroup(iCubSim_wrld_ctrl, bear_dict['model_list'], bear_dict['model_type'], [0, 1, 1], bear_dict['start_orient'], model_path + "/bear")
    print(bear.get_pos_model_group())
    time.sleep(4.)

    iCubSim_wrld_ctrl.del_all()
    del iCubSim_wrld_ctrl


if __name__ == '__main__':
    if params.GAZEBO_SIM:
        objects_gzbo()
    else:
        objects_iCubSim()
