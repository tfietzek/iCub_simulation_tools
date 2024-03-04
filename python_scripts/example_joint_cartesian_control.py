"""
Created on Mon Apr 28 2020

@author: Torsten Fietzek

joint cartesian control example

"""

import sys
import time

import numpy as np
import yarp


# Import parameter from parameter file
import example_parameter as params


T_r2w = params.Transfermat_robot2world
T_w2r = params.Transfermat_world2robot

######################################################################
# Init YARP network
yarp.Network.init()
if not yarp.Network.checkNetwork():
    sys.exit('[ERROR] Please try running yarp server')


######################################################################
# Example implementation using plain yarp
def cartesian_ctrl_yarp():
    ######################################################################
    # Init variables from parameter-file

    print('----- Init variables -----')
    pos = yarp.Vector(3)
    orient = yarp.Vector(4)

    orient_hand = yarp.Vector(params.orientation_robot_hand.shape[0])
    for i in range(params.orientation_robot_hand.shape[0]):
        orient_hand.set(i, params.orientation_robot_hand[i])

    ######################################################################
    # Init cartesian controller for right arm

    # Prepare a property object
    props = yarp.Property()
    props.put("device", "cartesiancontrollerclient")
    props.put("remote", "/" + params.ROBOT_PREFIX + "/cartesianController/right_arm")
    props.put("local", "/" + params.CLIENT_PREFIX + "/right_arm")

    # Create remote driver
    driver_rarm = yarp.PolyDriver(props)

    if not driver_rarm:
        sys.exit("Motor initialization failed!")

    # Query motor control interfaces
    iCart = driver_rarm.viewICartesianControl()
    iCart.setPosePriority("position")
    time.sleep(1)

    ######################################################################
    # Move hand to inital position and orientation
    print('----- Move hand to initial pose -----')
    welt_pos = params.pos_hand_world_coord
    init_hand_pos_r_np = np.dot(T_w2r, welt_pos.reshape((4, 1))).reshape((4,))
    init_hand_pos_r_yarp = yarp.Vector(init_hand_pos_r_np[0:3].shape[0])
    for i in range(init_hand_pos_r_np[0:3].shape[0]):
        init_hand_pos_r_yarp.set(i, init_hand_pos_r_np[0:3][i])

    iCart.goToPoseSync(init_hand_pos_r_yarp, orient_hand)
    iCart.waitMotionDone(timeout=5.0)
    time.sleep(1)
    iCart.getPose(pos, orient)
    print('Hand position:', pos.toString())
    print('Hand orientation:', orient.toString())

    ######################################################################
    # Move hand to new position and orientation
    print('----- Move hand to new pose -----')
    welt_pos_n = params.pos_hand_world_coord_new
    new_hand_pos_r_np = np.dot(T_w2r, welt_pos_n.reshape((4, 1))).reshape((4,))
    new_hand_pos_r_yarp = yarp.Vector(new_hand_pos_r_np[0:3].shape[0])
    for i in range(new_hand_pos_r_np[0:3].shape[0]):
        init_hand_pos_r_yarp.set(i, new_hand_pos_r_np[0:3][i])

    iCart.goToPoseSync(new_hand_pos_r_yarp, orient_hand)
    iCart.waitMotionDone(timeout=5.0)
    time.sleep(1)
    iCart.getPose(pos, orient)
    print('Hand position:', pos.toString())
    print('Hand orientation:', orient.toString())
    time.sleep(5)

    ######################################################################
    # Close network and motor cotrol
    print('----- Close control devices and opened ports -----')
    driver_rarm.close()
    yarp.Network.fini()


######################################################################
# Example implementation using iCub_Python_Lib-repo
def cartesian_ctrl_icub_pylib():
    # Import modules with specific functionalities
    import Python_libraries.YARP_motor_control as mot

    ######################################################################
    # Init variables from parameter-file
    print('----- Init variables -----')
    pos = yarp.Vector(3)
    orient = yarp.Vector(4)
    orient_hand = mot.npvec_2_yarpvec(params.orientation_robot_hand)

    ######################################################################
    # Init cartesian controller for right arm
    iCart, driver_rarm = mot.motor_init_cartesian(
        "right_arm", robot_prefix=params.ROBOT_PREFIX, client_prefix=params.CLIENT_PREFIX)

    if (not driver_rarm) or (not iCart):
        sys.exit("Motor initialization failed!")

    ######################################################################
    # Move hand to inital position and orientation
    print('----- Move hand to initial pose -----')
    welt_pos = params.pos_hand_world_coord
    init_hand_pos_r_np = np.dot(T_w2r, welt_pos.reshape((4, 1))).reshape((4,))
    init_hand_pos_r_yarp = mot.npvec_2_yarpvec(init_hand_pos_r_np[0:3])

    iCart.goToPoseSync(init_hand_pos_r_yarp, orient_hand)
    iCart.waitMotionDone(timeout=5.0)
    time.sleep(1)
    iCart.getPose(pos, orient)
    print('Hand position:', pos.toString())
    print('Hand orientation:', orient.toString())

    ######################################################################
    # Move hand to new position and orientation
    print('----- Move hand to new pose -----')
    welt_pos_n = params.pos_hand_world_coord_new
    new_hand_pos_r_np = np.dot(T_w2r, welt_pos_n.reshape((4, 1))).reshape((4,))
    new_hand_pos_r_yarp = mot.npvec_2_yarpvec(new_hand_pos_r_np[0:3])

    iCart.goToPoseSync(new_hand_pos_r_yarp, orient_hand)
    iCart.waitMotionDone(timeout=5.0)
    time.sleep(1)
    iCart.getPose(pos, orient)
    print('Hand position:', pos.toString())
    print('Hand orientation:', orient.toString())
    time.sleep(5)

    ######################################################################
    # Close network and motor cotrol
    print('----- Close control devices and opened ports -----')
    driver_rarm.close()
    yarp.Network.fini()


if __name__ == '__main__':
    if params.MODE == "yarp":
        cartesian_ctrl_yarp()
    elif params.MODE == "icub_pylib":
        cartesian_ctrl_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        raise NotImplementedError
    else:
        print("No valid MODE given! Check the example_parameter file!")
