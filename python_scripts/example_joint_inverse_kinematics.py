"""
Created on Thu Sep 22 17:53:33 CEST 2022

@author: Torsten Fietzek

example for joint inverse kinematics

"""

######################################################################
########################## Import modules  ###########################
######################################################################
import sys
import time

import numpy as np

import Python_libraries.YARP_motor_control as mot
import Python_libraries.iCub_transformation_matrices as iTransform

################ Import parameter from parameter file ################
import example_parameter as params


# position control with yarp commands
def inverse_kin_yarp():
    import icub

    # Set up kinematic chain for the iCub -> here right arm
    iCub_arm = icub.iCubArm("right_v2")
    iCub_arm_chain = iCub_arm.asChain()

    joint_angles = np.deg2rad(np.array([15., 16., 0., 70., -90., 0., 0.]))
    iCub_arm.setAng(mot.npvec_2_yarpvec(joint_angles))

    print("DOF:", iCub_arm.getDOF())

    # Prepare the solver for the inverse kinematics from the iKin-library
    # IKINCTRL_POSE_XYZ -> only solve for translational position not for rotation
    # IKINCTRL_POSE_ANG -> only solve for rotation not for translational position
    # IKINCTRL_POSE_FULL -> solve for translational position and for rotation
    solver = icub.iKinIpOptMin(iCub_arm_chain, icub.IKINCTRL_POSE_XYZ, 1e-3, 1e-6, 100)
    solver.setUserScaling(True,100.0,100.0,100.0)

    # Solve the inverse kinemtics for the given goal
    goal = np.array([-0.25, 0., 0.35])
    goal_yarp = mot.npvec_2_yarpvec(goal)
    angles = mot.yarpvec_2_npvec(solver.solve(iCub_arm.getAng(), goal_yarp))

    print("Goal:", goal, "\nReached Position:", np.round(mot.yarpvec_2_npvec(iCub_arm.EndEffPosition()), 2))
    print("\nInitial Joint angles:", np.round(np.degrees(joint_angles), 2))
    print("Target Joint angles:", np.round(np.degrees(angles), 2))


# position control with icub pylib methods
def inverse_kin_icub_pylib():
    raise NotImplementedError("Function not yet implemented!")


# position control with iCub-ANNarchy-Interface
def inverse_kin_ANN_iCub_Interface():
    if len(params.PATH_TO_INTERFACE_BUILD) > 0:
        sys.path.append(params.PATH_TO_INTERFACE_BUILD)

    import ANN_iCub_Interface.Vocabs as iCub_Const
    from ANN_iCub_Interface.iCub import Kinematic_Writer, iCub_Interface

    ######################################################################
    ###################### Add interface instances #######################
    ######################################################################

    # Interface main wrapper, is needed once
    iCub = iCub_Interface.ANNiCub_wrapper()

    # Add kinematic writer instance
    kinwriter = Kinematic_Writer.PyKinematicWriter()

    # Init kinematic writer
    print('Init kinematic writer')
    if not kinwriter.init(iCub, "invkin", part=iCub_Const.PART_KEY_RIGHT_ARM, version=2, ini_path=params.INTERFACE_INI_PATH, offline_mode=params.offline):
        sys.exit("Initialization failed")

    target_position = [-0.3, 0.0, 0.05]
    blocked_joints = [0, 1, 2, 7, 8, 9]  # [0, 1, 2] -> all joints of the torso part; [7, 8, 9] -> joints [4, 5, 6] of arm part
    joint_angles = np.deg2rad(np.array([-20., 5., 30., 30.]))

    print("Current joint angles:", np.rad2deg(kinwriter.get_jointangles()))
    print("DOF:", kinwriter.get_DOF())

    ######################################################################
    # Perform inverse kinematic: Either offline with manually set starting angles or online with the current angles retrieved from the robot
    if params.offline:
        kinwriter.block_links(blocked_joints)
        kinwriter.set_jointangles(joint_angles)
        joint_angles = kinwriter.solve_InvKin(target_position)
    else:
        joint_angles = kinwriter.solve_InvKin(target_position, blocked_joints)
    print("Estimated joint angles:", np.rad2deg(joint_angles))


    ######################################################################
    ###################### Close interface instances #####################
    print('----- Close interface instances -----')
    iCub.clear()


if __name__ == '__main__':
    if params.MODE == "yarp":
        inverse_kin_yarp()
    elif params.MODE == "icub_pylib":
        inverse_kin_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        inverse_kin_ANN_iCub_Interface()
    else:
        print("No valid MODE given! Check the example_parameter file!")
