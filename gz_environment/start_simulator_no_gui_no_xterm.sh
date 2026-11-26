
#!/bin/bash

if [ $# -eq 0 ]; then
    file="./icub_image_visuomanip"
else
    file="$1"
fi

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"

#### Start yarpserver
echo "Starting yarpserver..."
yarpserver --write > "$LOG_DIR/yarpserver.log" 2>&1 &
YARP_PID=$!

echo "Started yarpserver (PID: $YARP_PID)"

sleep 1

#### Start Gazebo simulator
echo "Starting Gazebo simulator..."
DISPLAY= gz sim -v 4 -s -r --headless-rendering "$file.sdf" \
    > "$LOG_DIR/gazebo.log" 2>&1 &
GAZEBO_PID=$!

echo "Started Gazebo simulator (PID: $GAZEBO_PID)"

wait

