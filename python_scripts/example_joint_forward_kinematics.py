"""
Created on Thu Sep 22 17:53:33 CEST 2022

@author: Torsten Fietzek

example for joint forward kinematic

"""

import sys
import time

import numpy as np

import example_parameter as params
import Python_libraries.iCub_transformation_matrices as iTransform


######################################################################
# Example implementation using plain yarp
def forward_kin_yarp():
    import icub

    import Python_libraries.YARP_motor_control as mot

    iCub_arm = icub.iCubArm("right_v2")

    # Release torso links if they stay static and at zero position
    # iCub_arm.releaseLink(0)
    # iCub_arm.releaseLink(1)
    # iCub_arm.releaseLink(2)

    joint_angles = np.deg2rad(np.array([15., 16., 0., 70., -90., 0., 0.]))
    iCub_arm.setAng(mot.npvec_2_yarpvec(joint_angles))

    print("DOF:", iCub_arm.getDOF())

    # Select robot -> world transforamtion matrix dependent on used simulator -> Gazebo or iCub-Simulator
    if params.GAZEBO_SIM:
        Transfermat_robot2world = iTransform.Transfermat_robot2gazebo
    else:
        Transfermat_robot2world = iTransform.Transfermat_robot2iCubSim

    end_eff_pos = mot.yarpvec_2_npvec(iCub_arm.EndEffPosition())
    print("End-Effector", end_eff_pos)  # (robot reference frame)
    print("End-Effector", iTransform.transform_position(end_eff_pos,
          Transfermat_robot2world))  # (simulator reference frame)

    # Retrieve position for specific joint of the kinematic chain
    joint3_pos = mot.yarpvec_2_npvec(iCub_arm.Position(3))
    print("Joint 3", joint3_pos)    # (robot reference frame)
    print("Joint 3", iTransform.transform_position(joint3_pos, Transfermat_robot2world))    # (simulator reference frame)


######################################################################
# Example implementation using iCub_Python_Lib-repo
def forward_kin_icub_pylib():
    raise NotImplementedError("Function not yet implemented!")


######################################################################
# Example implementation using the ANNarchy-iCub-Interface
def forward_kin_ANN_iCub_Interface():
    if len(params.PATH_TO_INTERFACE_BUILD) == 0:
        import ANN_iCub_Interface.iCub as iCub_mod
        import ANN_iCub_Interface.Vocabs as iCub_const
    else:
        sys.path.append(params.PATH_TO_INTERFACE_BUILD)
        import ANN_iCub_Interface.iCub as iCub_mod
        import ANN_iCub_Interface.Vocabs as iCub_const

    ######################################################################
    # Add interface instances

    # Interface main wrapper, is needed once
    iCub = iCub_mod.iCub_Interface.ANNiCub_wrapper()

    # Add kinematic reader instance
    kinreader = iCub_mod.Kinematic_Reader.PyKinematicReader()

    # Init kinematic reader
    print('Init kinematic reader')
    if not kinreader.init(iCub, "fkin", part=iCub_const.PART_KEY_RIGHT_ARM, version=2, ini_path="./data/", offline_mode=params.offline):
        sys.exit("Init failed")

    if params.offline:
        kinreader.block_links([0, 1, 2])
        joint_angles = np.deg2rad(np.array([15., 16., 0., 70., -90., 0., 0.]))
        kinreader.set_jointangles(joint_angles)

    print("DOF:", kinreader.get_DOF())

    # Select robot -> world transforamtion matrix dependent on used simulator -> Gazebo or iCub-Simulator
    if params.GAZEBO_SIM:
        Transfermat_robot2world = iTransform.Transfermat_robot2gazebo
    else:
        Transfermat_robot2world = iTransform.Transfermat_robot2iCubSim

    # print end-effector position
    end_eff_pos = kinreader.get_handposition()
    print("End-Effector", end_eff_pos)  # (robot reference frame)
    print("End-Effector", iTransform.transform_position(end_eff_pos,
          Transfermat_robot2world))  # (simulator reference frame)

    # print position for specific joint of the kinematic chain
    joint3_pos = kinreader.get_jointposition(3)
    print("Joint 3", joint3_pos)    # (robot reference frame)
    print("Joint 3", iTransform.transform_position(joint3_pos, Transfermat_robot2world))    # (simulator reference frame)

    # Close kinematic reader module
    kinreader.close(iCub)

    ######################################################################
    # Close interface instances
    print('----- Close interface instances -----')
    iCub.clear()


if __name__ == '__main__':
    if params.MODE == "yarp":
        forward_kin_yarp()
    elif params.MODE == "icub_pylib":
        forward_kin_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        forward_kin_ANN_iCub_Interface()
    else:
        print("No valid MODE given! Check the example_parameter file!")
