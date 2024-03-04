"""
Created on Tue July 07 2020

@author: Torsten Fietzek

Tactile perception example

"""

import sys
import time

import numpy as np
import yarp

import example_parameter as params


######################################################################
# Init YARP network
print('----- Init network -----')
yarp.Network.init()
if not yarp.Network.checkNetwork():
    sys.exit('[ERROR] Please try running yarp server')


######################################################################
# Example implementation using plain yarp
def tactile_prcptn_yarp():
    ######################################################################
    # Open and connect YARP-Ports to read right arm skin sensor data

    # Upper arm section
    input_port_skin_rarm = yarp.Port()
    if not input_port_skin_rarm.open("/" + params.CLIENT_PREFIX + "/skin_read/rarm"):
        print("[ERROR] Could not open skin arm port")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/skin/right_arm_comp", input_port_skin_rarm.getName()):
        print("[ERROR] Could not connect skin arm port!")

    # Forearm skin section
    input_port_skin_rforearm = yarp.Port()
    if not input_port_skin_rforearm.open("/" + params.CLIENT_PREFIX + "/skin_read/rforearm"):
        print("[ERROR] Could not open skin forearm port!")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/skin/right_forearm_comp", input_port_skin_rforearm.getName()):
        print("[ERROR] Could not connect skin forearm port!")

    # Hand skin section
    input_port_skin_rhand = yarp.Port()
    if not input_port_skin_rhand.open("/" + params.CLIENT_PREFIX + "/skin_read/rhand"):
        print("[ERROR] Could not open skin hand port!")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/skin/right_hand_comp", input_port_skin_rhand.getName()):
        print("[ERROR] Could not connect skin hand port!")

    ######################################################################
    # Read skin sensor data
    for i in range(10):
        ######################################################################
        # Retrieve data from the ports

        tactile_rarm = yarp.Vector(768)
        while (not input_port_skin_rarm.read(tactile_rarm)):
            yarp.delay(0.001)

        tactile_rforearm = yarp.Vector(384)
        while (not input_port_skin_rforearm.read(tactile_rforearm)):
            yarp.delay(0.001)

        tactile_rhand = yarp.Vector(192)
        while (not input_port_skin_rhand.read(tactile_rhand)):
            yarp.delay(0.001)

        ######################################################################
        # select real sensor data from raw signal stream -> not each data point has a respective sensor
        data_rarm = []
        data_rforearm = []
        data_rhand = []

        for j in range(len(params.skin_idx_r_arm)):
            if params.skin_idx_r_arm[j] > 0:
                data_rarm.append(tactile_rarm.get(j))

        for j in range(len(params.skin_idx_r_forearm)):
            if params.skin_idx_r_forearm[j] > 0:
                data_rforearm.append(tactile_rforearm.get(j))

        for j in range(len(params.skin_idx_r_hand)):
            if params.skin_idx_r_hand[j] > 0:
                data_rhand.append(tactile_rhand.get(j))

        print("Data arm:")
        print(data_rarm)

        print("Data forearm:")
        print(data_rforearm)

        print("Data hand:")
        print(data_rhand)

        time.sleep(2.0)

    ######################################################################
    # Closing the program: Close ports and network
    print('----- Close opened ports -----')

    # disconnect the ports
    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/skin/right_arm_comp", input_port_skin_rarm.getName()):
        print("[ERROR] Could not disconnect skin arm port!")

    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/skin/right_forearm_comp", input_port_skin_rforearm.getName()):
        print("[ERROR] Could not disconnect skin forearm port!")

    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/skin/right_hand_comp", input_port_skin_rhand.getName()):
        print("[ERROR] Could not disconnect skin hand port!")

    # close the ports
    input_port_skin_rarm.close()
    input_port_skin_rforearm.close()
    input_port_skin_rhand.close()

    yarp.Network.fini()


######################################################################
# Example implementation using the ANNarchy-iCub-Interface
def tactile_prcptn_iCub_ANN():
    if len(params.PATH_TO_INTERFACE_BUILD) == 0:
        import ANN_iCub_Interface.iCub as iCub_mod
        from ANN_iCub_Interface.iCub import Skin_Reader
        import ANN_iCub_Interface.Vocabs as iCub_const
    else:
        sys.path.append(params.PATH_TO_INTERFACE_BUILD)
        import ANN_iCub_Interface.iCub as iCub_mod
        import ANN_iCub_Interface.Vocabs as iCub_const

    ######################################################################
    # Add interface instances

    # Interface main wrapper, is needed once
    iCub = iCub_mod.iCub_Interface.ANNiCub_wrapper()

    # Add skin reader instance
    sreader = Skin_Reader.PySkinReader()

    # Init interface instances
    sreader.init(iCub, "skin_right", "r", True, ini_path=params.INTERFACE_INI_PATH)

    ######################################################################
    # Read skin sensor data -> buffered
    for i in range(10):
        # read tactile data
        sreader.read_tactile()

        # print tactile data
        print("Data arm:")
        print(sreader.get_tactile_arm())

        print("Data forearm:")
        print(sreader.get_tactile_forearm())

        print("Data hand:")
        print(sreader.get_tactile_hand())

    ######################################################################
    # Read skin sensor data -> skin section specific
    for i in range(10):
        # print tactile data
        print("Data arm:")
        print(sreader.read_skin_arm())

        print("Data forearm:")
        print(sreader.read_skin_forearm())

        print("Data hand:")
        print(sreader.read_skin_hand())

    ######################################################################
    # Close interface instances
    sreader.close(iCub)


if __name__ == '__main__':
    if params.MODE == "yarp":
        tactile_prcptn_yarp()
    elif params.MODE == "icub_pylib":
        raise NotImplementedError
    elif params.MODE == "iCub_ANN":
        tactile_prcptn_iCub_ANN()
    else:
        print("No valid MODE given! Check the example_parameter file!")