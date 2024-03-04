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

import matplotlib.image as img_save
import matplotlib.pylab as plt
import numpy as np
import yarp

################ Import parameter from parameter file ################
import example_parameter as params


def scene_cam_yarp():
    ######################################################################
    ######################### Init YARP network ##########################

    print('----- Init network -----')
    # network initialization and check
    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        print('[ERROR] Please try running yarp server')

    print('----- Open port -----')
    # Initialization of all needed ports
    # Port for scene image
    input_port_scene = yarp.Port()
    if not input_port_scene.open("/" + params.CLIENT_PREFIX + "/scene"):
        print("[ERROR] Could not open scene camera port")
    if not yarp.Network.connect("/" + params.ROBOT_PREFIX + "/cam", "/" + params.CLIENT_PREFIX + "/scene"):
        print("[ERROR] Could not connect input_port_scene")


    ######################################################################
    ############### Initialization of imgae data structures ##############

    scene_img_array = np.ones((240, 320, 3), np.uint8)
    scene_yarp_image = yarp.ImageRgb()
    scene_yarp_image.resize(320, 240)

    scene_yarp_image.setExternal(scene_img_array.data, scene_img_array.shape[1], scene_img_array.shape[0])


    ######################################################################
    ################### Read camera images from robot ####################
    print('----- Read images from robot cameras -----')
    camera_imgs = []
    for i in range(5):
        print("Image:", i)
        # Read the images from the robot cameras
        input_port_scene.read(scene_yarp_image)
        input_port_scene.read(scene_yarp_image)

        if scene_yarp_image.getRawImage().__int__() != scene_img_array.__array_interface__['data'][0]:
            print("read() reallocated my scene_yarp_image!")
        camera_imgs.append(scene_img_array.copy())
        # show images
        plt.figure(figsize=(10,5))
        plt.tight_layout()
        plt.title("Scene camera image")
        plt.imshow(scene_img_array)
        plt.show()
        # time.sleep(0.025)


    subdir = "./scene"
    if not os.path.isdir(subdir):
        os.mkdir(subdir)

    for idx, img in enumerate(camera_imgs):
        img_save.imsave(subdir + '/scene' + str(idx) + '.png', img)

    ######################################################################
    ######################## Closing the program: ########################
    #### Delete objects/models and close ports, network, motor cotrol ####
    print('----- Close opened ports -----')

    # disconnect the ports
    if not yarp.Network.disconnect("/" + params.ROBOT_PREFIX + "/cam", input_port_scene.getName()):
        print("[ERROR] Could not disconnect input_port_scene")


    # close the ports
    input_port_scene.close()

    # close the yarp network
    yarp.Network.fini()


def scene_cam_icub_pylib():
    # TODO: implement example
    raise NotImplementedError("Not yet implemented!")


if __name__ == '__main__':
    if params.MODE == "yarp":
        scene_cam_yarp()
    elif params.MODE == "icub_pylib":
        scene_cam_icub_pylib()
    elif params.MODE == "ANN_iCub_Interface":
        raise NotImplementedError("This is not planned to be implemented!")
    else:
        print("No valid MODE given! Check the example_parameter file!")
