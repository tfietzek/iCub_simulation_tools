"""
Created on Tue July 07 2020

@author: Torsten Fietzek

Visual perception example

"""

import sys

import matplotlib.pylab as plt
import numpy as np
import yarp

import example_parameter as params


######################################################################
# Example implementation using plain yarp
def visual_input_yarp():
    ######################################################################
    # Init YARP network

    print('----- Init network -----')
    # network initialization and check
    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        print('[ERROR] Please try running yarp server')

    print('----- Open ports -----')
    # Initialization of all needed ports
    # Port for right eye image
    input_port_right_eye = yarp.Port()
    if not input_port_right_eye.open("/" + params.CLIENT_PREFIX + "/eyes/right"):
        print("[ERROR] Could not open right eye port")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/cam/right", "/" + params.CLIENT_PREFIX + "/eyes/right"):
        print("[ERROR] Could not connect input_port_right_eye")

    # Port for left eye image
    input_port_left_eye = yarp.Port()
    if not input_port_left_eye.open("/" + params.CLIENT_PREFIX + "/eyes/left"):
        print("[ERROR] Could not open left eye port")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/cam/left", "/" + params.CLIENT_PREFIX + "/eyes/left"):
        print("[ERROR] Could not connect input_port_left_eye")

    ######################################################################
    # Initialization of both eye images

    print('----- Init image array structures -----')
    # Create numpy array to receive the image and the YARP image wrapped around it
    left_eye_img_array = np.ones((240, 320, 3), np.uint8)
    left_eye_yarp_image = yarp.ImageRgb()
    left_eye_yarp_image.resize(320, 240)

    right_eye_img_array = np.ones((240, 320, 3), np.uint8)
    right_eye_yarp_image = yarp.ImageRgb()
    right_eye_yarp_image.resize(320, 240)

    left_eye_yarp_image.setExternal(
        left_eye_img_array.data, left_eye_img_array.shape[1], left_eye_img_array.shape[0])
    right_eye_yarp_image.setExternal(
        right_eye_img_array.data, right_eye_img_array.shape[1], right_eye_img_array.shape[0])

    ######################################################################
    # Read camera images from robot
    print('----- Read images from robot cameras -----')
    for i in range(5):
        print("Image:", i)
        # read ports twice to make sure a the full image arrived
        input_port_left_eye.read(left_eye_yarp_image)
        input_port_left_eye.read(left_eye_yarp_image)
        input_port_right_eye.read(right_eye_yarp_image)
        input_port_right_eye.read(right_eye_yarp_image)

        if left_eye_yarp_image.getRawImage().__int__() != left_eye_img_array.__array_interface__['data'][0]:
            print("read() reallocated my left_eye_yarp_image!")
        if right_eye_yarp_image.getRawImage().__int__() != right_eye_img_array.__array_interface__['data'][0]:
            print("read() reallocated my right_eye_yarp_image!")

        # show images
        plt.figure(figsize=(10, 5))
        plt.tight_layout()
        plt.subplot(121)
        plt.title("Left camera image")
        plt.imshow(left_eye_img_array)

        plt.subplot(122)
        plt.title("Right camera image")
        plt.imshow(right_eye_img_array)
        plt.show()

    ######################################################################
    # Closing the program: Close ports and network
    print('----- Close opened ports -----')

    # disconnect the ports
    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/cam/right", input_port_right_eye.getName()):
        print("[ERROR] Could not disconnect input_port_right_eye")

    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/cam/left", input_port_left_eye.getName()):
        print("[ERROR] Could not disconnect input_port_left_eye")

    # close the ports
    input_port_right_eye.close()
    input_port_left_eye.close()

    # close the yarp network
    yarp.Network.fini()


######################################################################
# Example implementation using iCub_Python_Lib-repo
def visual_input_icub_pylib():
    # Import modules with specific functionalities
    import Python_libraries.YARP_image_processing as img_proc
    import Python_libraries.YARP_network_control as net_ctrl

    ######################################################################
    # Init YARP network
    print('----- Open ports -----')
    port_right, port_left = net_ctrl.network_init_binocular(params.CLIENT_PREFIX, params.ROBOT_PREFIX)

    ######################################################################
    # Initialization of both eye images
    print('----- Init image array structures -----')
    yarp_img_r, np_arr_r, yarp_img_l, np_arr_l = img_proc.define_eye_imgs()

    ######################################################################
    # Read camera images from robot
    print('----- Read images from robot cameras -----')
    for i in range(5):
        np_img_r, np_img_l = img_proc.read_robot_eyes(port_right, port_left, yarp_img_r, yarp_img_l, np_arr_r, np_arr_l)

        # show images
        plt.figure(figsize=(10, 5))
        plt.tight_layout()
        plt.subplot(121)
        plt.title("Left camera image")
        plt.imshow(np_img_l)

        plt.subplot(122)
        plt.title("Right camera image")
        plt.imshow(np_img_r)
        plt.show()

    ######################################################################
    # Closing the program: Close ports and network
    net_ctrl.network_clean_binocular(port_right, port_left, params.ROBOT_PREFIX)


######################################################################
# Example implementation using the ANNarchy-iCub-Interface
def visual_input_ANN_iCub_Interface():
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

    # Add visual reader instance
    visreader = iCub_mod.Visual_Reader.PyVisualReader()
    visreader_r = iCub_mod.Visual_Reader.PyVisualReader()
    visreader_l = iCub_mod.Visual_Reader.PyVisualReader()

    # Init interface instances
    visreader.init(iCub, "both", 'b', ini_path=params.INTERFACE_INI_PATH)
    visreader_r.init(iCub, "right", 'r', ini_path=params.INTERFACE_INI_PATH)
    visreader_l.init(iCub, "left", 'l', ini_path=params.INTERFACE_INI_PATH)

    ######################################################################
    # Read camera images from robot

    # grayscale images; preprocessed -> range [0., 1.]
    test_imgs = visreader.read_robot_eyes()
    test_imgs = test_imgs.reshape(2, 240, 320)

    plt.figure(figsize=(10, 5))
    plt.tight_layout()
    plt.subplot(121)
    plt.title("Left camera image")
    plt.imshow(test_imgs[1], cmap="gray")

    plt.subplot(122)
    plt.title("Right camera image")
    plt.imshow(test_imgs[0], cmap="gray")
    plt.show()

    # RGB images; no preprocessing -> range [0, 255]
    imgleft = np.array(visreader_l.retrieve_robot_eye()).reshape(240, 320, 3)
    imgright = np.array(visreader_r.retrieve_robot_eye()).reshape(240, 320, 3)

    plt.figure(figsize=(10, 5))
    plt.tight_layout()
    plt.subplot(121)
    plt.title("Left camera image")
    plt.imshow(imgleft)

    plt.subplot(122)
    plt.title("Right camera image")
    plt.imshow(imgright)
    plt.show()

    ######################################################################
    # Close interface instances
    iCub.clear()


if __name__ == '__main__':
    if params.MODE == "yarp":
        visual_input_yarp()
    elif params.MODE == "icub_pylib":
        visual_input_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        visual_input_ANN_iCub_Interface()
    else:
        print("No valid MODE given! Check the example_parameter file!")
