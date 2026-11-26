
#!/bin/bash

# Starts the yarpserver and the Gazebo simulator with the iCub inside

if [ $# -eq 0 ]; then
    file="icub_image_visuomanip"
else
    file="$1"
fi

# Create log directory
LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

#### Start yarpserver
echo "Starting yarpserver..."
yarpserver --write > "$LOG_DIR/yarpserver.log" 2>&1 &
YARP_PID=$!
echo "Started yarpserver (PID: $YARP_PID)"
echo "Log: $LOG_DIR/yarpserver.log"

sleep 1

#### Start iCub simulator
echo "Starting Gazebo simulator..."
gz sim -v 4 "$file.sdf" > "$LOG_DIR/gazebo.log" 2>&1 &
GAZEBO_PID=$!
echo "Started Gazebo simulator (PID: $GAZEBO_PID)"
echo "Log: $LOG_DIR/gazebo.log"

# Wait for both processes
wait

