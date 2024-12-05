The 3 scripts act as a shortcut to create or delete a conda environment for the work with the iCub robot.

1. Open a terminal and start the install script (skip if conda is already installed):
```bash
    bash install_icub_conda.sh
```

2. After reopening the terminal run the prepare script, which takes as an optional argument the environment name. Otherwise it is set to "iCub":
```bash
    bash prepare_icub_conda.sh env_name
```

3. The environment should be ready for work. After a restart of the terminal it can be activated either with "mamba activate iCub" or "iCub" which is set as an alias for the first command.

4. If conda is not used anymore, the third script can be used for a cleanup, deleting the !!whole conda installation!! and the entries in the bashrc (should only be used, if conda is installed via "install_icub_conda.sh"):
```bash
    bash remove_icub_conda.sh
```

Additional:
- a backup of the .bashrc-file is done in the prepare-script as well as in the remove-script to avoid loss of information
- only the iCub-related packages are installed yet, ANNarchy as well as the ANN-iCub-Interface need to be installed manually