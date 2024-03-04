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

################ Import parameter from parameter file ################
import example_parameter as params


# position control with yarp commands
def inverse_kin_yarp():
    import icub
    raise NotImplementedError
    # TODO: add implementation





# position control with icub pylib methods
def inverse_kin_icub_pylib():
    raise NotImplementedError("Function not yet implemented!")


# position control with iCub-ANNarchy-Interface
def inverse_kin_ANN_iCub_Interface():
    if len(params.PATH_TO_INTERFACE_BUILD) == 0:
        import ANN_iCub_Interface.iCub as iCub_mod
        import ANN_iCub_Interface.Vocabs as iCub_const
    else:
        sys.path.append(params.PATH_TO_INTERFACE_BUILD)
        import ANN_iCub_Interface.iCub as iCub_mod
        import ANN_iCub_Interface.Vocabs as iCub_const

    ######################################################################
    ###################### Add interface instances #######################
    # top module
    iCub = iCub_mod.iCub_Interface.ANNiCub_wrapper()

    raise NotImplementedError
    # TODO: finish implementation


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
