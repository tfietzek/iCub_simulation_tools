#!/bin/bash

# starts the whole simulation in one terminal: yarpserver, gazebo server and GUI, cartesian controller and solvers
# each program is started after the previous one is ready, the outputs are written to logs/
# usage: bash start_all.sh (world_filename) (--no-gui)
# stop everything with Ctrl+C

cd "$(dirname "$0")"

world="icub_image_visuomanip"
gui=true
for arg in "$@"
do
    case $arg in
        --no-gui) gui=false ;;
        *) world=$arg ;;
    esac
done

world_file="gazebo_config/worlds/${world%.sdf}.sdf"
[ -f "$world_file" ] || world_file="${world%.sdf}.sdf" # otherwise let gazebo search the GZ_SIM_RESOURCE_PATH

parts="right_arm left_arm"
logdir="$PWD/logs"
mkdir -p "$logdir"

pids=()

stop_all() {
    echo "stop all programs"
    kill "${pids[@]}" 2>/dev/null
    sleep 2
    kill -9 "${pids[@]}" 2>/dev/null
    exit
}
trap stop_all INT TERM

# start a program in the background, $1: log name, rest: command
start() {
    local name=$1
    shift
    echo "run $name"
    "$@" > "$logdir/$name.log" 2>&1 &
    pids+=($!)
}

# repeat a check until it succeeds, $1: description, $2: timeout in s, rest: check command
wait_for() {
    local what=$1 timeout=$2
    shift 2
    printf "wait for %s " "$what"
    for ((i = 0; i < timeout; i++))
    do
        if "$@" > /dev/null 2>&1
        then
            echo "ok"
            return
        fi
        printf "."
        sleep 1
    done
    echo "failed, see $logdir"
    stop_all
}

#### start yarpserver
start yarpserver yarpserver --write
wait_for "yarpserver" 20 yarp exists /root

#### start gazebo server and GUI
# exec, so that the stored pid is the one of the simulator process
start gazebo_server bash -c "exec gz sim -s -r -v 3 $world_file"
wait_for "iCub in gazebo" 120 yarp exists /icubSim/torso/rpc:i

if $gui
then
    start gazebo_gui bash -c "exec gz sim -g"
fi

#### start cartesian controller and solvers
start cartesian_controller yarprobotinterface --context gazeboCartesianControl
for part in $parts
do
    start solver_$part iKinCartesianSolver --context gazeboCartesianControl --part $part
done
for part in $parts
do
    wait_for "cartesian solver $part" 60 grep -q "cartesianSolver/$part is alive... ready" "$logdir/cartesian_controller.log"
done

echo "simulation is ready, stop it with Ctrl+C"
wait
