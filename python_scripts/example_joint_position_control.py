"""
Created on Mon Apr 28 2020

@author: Torsten Fietzek

joint position control example

"""

import sys
import time

import numpy as np
import yarp

import example_parameter as params


######################################################################
# Example implementation using plain yarp
def position_ctrl_yarp():
    # Import modules with specific functionalities
    import Python_libraries.YARP_motor_control as mot

    ######################################################################
    # Init YARP network
    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        sys.exit('[ERROR] Please try running yarp server')

    # Init motor control for the head
    print('----- Init head motor control -----')

    props = yarp.Property()
    props.put("device", "remote_controlboard")
    props.put("local", "/" + params.CLIENT_PREFIX + "/head")
    props.put("remote", "/" + params.ROBOT_PREFIX + "/head")

    # create remote driver
    Driver_head = yarp.PolyDriver(props)

    if not Driver_head:
        sys.exit("Motor initialization failed!")

    # query motor control interfaces
    iPos_head = Driver_head.viewIPositionControl()
    iEnc_head = Driver_head.viewIEncoders()

    # retrieve number of joints
    jnts_head = iPos_head.getAxes()

    ######################################################################
    # Go to head zero position
    mot.goto_zero_head_pos(iPos_head, iEnc_head, jnts_head)

    ######################################################################
    # Move the head to predefined position
    print('----- Move head absolute -----')
    new_pos = yarp.Vector(jnts_head)
    pos = np.array([5., 0., -25., 0., 25., 10.])
    for i in range(jnts_head):
        new_pos.set(i, pos[i])

    motion = not (iPos_head.positionMove(new_pos.data()))
    yarp.delay(0.01)
    # optional, for blocking while moving the joints
    while not motion:
        motion = iPos_head.checkMotionDone()

    ######################################################################
    # Retrieve head joints position
    yarp_angles = yarp.Vector(jnts_head)
    read = iEnc_head.getEncoders(yarp_angles.data())
    while not read:
        time.sleep(0.01)
        read = iEnc_head.getEncoders(yarp_angles.data())

    vector = np.zeros(yarp_angles.length(), dtype=np.float64)
    for i in range(yarp_angles.length()):
        vector[i] = yarp_angles.get(i)

    print(vector)
    time.sleep(4.)

    ######################################################################
    # Move the head relative to the current position
    print('----- Move head relative -----')
    new_rel_pos = yarp.Vector(jnts_head)
    rel_pos = -pos
    for i in range(jnts_head):
        new_pos.set(i, pos[i])
    iPos_head.relativeMove(new_pos.data())

    ######################################################################
    # Retrieve head joints position
    yarp_angles = yarp.Vector(jnts_head)
    read = iEnc_head.getEncoders(yarp_angles.data())
    while not read:
        time.sleep(0.01)
        read = iEnc_head.getEncoders(yarp_angles.data())

    vector = np.zeros(yarp_angles.length(), dtype=np.float64)
    for i in range(yarp_angles.length()):
        vector[i] = yarp_angles.get(i)

    print(vector)
    time.sleep(4.)

    ######################################################################
    # Go to head zero position
    mot.goto_zero_head_pos(iPos_head, iEnc_head, jnts_head)

    ######################################################################
    # Close network and motor cotrol
    print('----- Close control devices and opened ports -----')
    Driver_head.close()
    yarp.Network.fini()


######################################################################
# Example implementation using iCub_Python_Lib-repo
def position_ctrl_icub_pylib():
    # Import modules with specific functionalities
    import Python_libraries.YARP_motor_control as mot

    ######################################################################
    # Init motor control for the head
    print('----- Init head motor control -----')
    iPos_head, iEnc_head, jnts_head, driver_head = mot.motor_init("head", control="position", robot_prefix=params.ROBOT_PREFIX, client_prefix=params.CLIENT_PREFIX)

    if not driver_head:
        sys.exit("Motor initialization failed!")

    ######################################################################
    # Go to head zero position
    mot.goto_zero_head_pos(iPos_head, iEnc_head, jnts_head)

    ######################################################################
    # Move the head to predefined position
    print('----- Move head absolute -----')
    new_pos = mot.set_pos_vector_array(np.array([5., 0., -25., 0., 25., 10.]), jnts_head)

    # Move to a position with blocking until motion is done
    # if blocking is not need simple use iPos_head.positionMove(new_pos.data())
    mot.goto_position_block(iPos_head, iEnc_head, jnts_head, new_pos)

    # Move the head to relative position
    # print('----- Move head relative -----')
    # No specific function for relative motion yet

    ######################################################################
    # Retrieve head joints position
    vector = mot.yarpvec_2_npvec(mot.get_joint_position(iEnc_head, jnts_head))
    print(vector)
    time.sleep(4.)

    ######################################################################
    # Go to head zero position
    mot.goto_zero_head_pos(iPos_head, iEnc_head, jnts_head)

    ######################################################################
    # Close network and motor cotrol
    print('----- Close control devices and opened ports -----')
    driver_head.close()
    yarp.Network.fini()


######################################################################
# Example implementation using the ANNarchy-iCub-Interface
def position_ctrl_ANN_iCub_Interface():
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

    # Reader/Writer instances
    reader = iCub_mod.Joint_Reader.PyJointReader()
    writer = iCub_mod.Joint_Writer.PyJointWriter()

    # Init interface instances
    reader.init(iCub, "read_head", iCub_const.PART_KEY_HEAD, 0.5, 15, ini_path=params.INTERFACE_INI_PATH)
    writer.init(iCub, "write_head", iCub_const.PART_KEY_HEAD, 0.5, 15, ini_path=params.INTERFACE_INI_PATH)

    ######################################################################
    # Go to head zero position
    writer.write_double_all([0., 0., 0., 0., 0., 0.], mode="abs", blocking=True)

    ######################################################################
    # Move the head to predefined position
    print('----- Move head absolute -----')
    new_pos = np.array([5., 0., -25., 0., 25., 10.])
    writer.write_double_all(new_pos, mode="abs", blocking=True)

    ######################################################################
    # Retrieve head joints position
    print(reader.read_double_all())
    time.sleep(3.)

    ######################################################################
    # Move the head relative to the current position
    print('----- Move head relative -----')
    rel_pos = -new_pos
    writer.write_double_all(rel_pos, mode="rel", blocking=True)

    ######################################################################
    # Retrieve head joints position
    print(reader.read_double_all())
    time.sleep(3.)

    ######################################################################
    # Go to head zero position
    writer.write_double_all([0., 0., 0., 0., 0., 0.], mode="abs", blocking=True)

    ######################################################################
    # Close interface instances
    print('----- Close interface instances -----')
    iCub.clear()


if __name__ == '__main__':
    if params.MODE == "yarp":
        position_ctrl_yarp()
    elif params.MODE == "icub_pylib":
        position_ctrl_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        position_ctrl_ANN_iCub_Interface()
    else:
        print("No valid MODE given! Check the example_parameter file!")
