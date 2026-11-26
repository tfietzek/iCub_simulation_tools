#!/bin/bash

# starts the red ball demo in one terminal: simulation with cartesian controller (start_all.sh),
# the moving red ball and the demo itself
# usage: bash start_redball.sh (--no-gui) (--static) (--no-reach) (--show)
#   --no-gui   -> start gazebo without GUI-client
#   --static   -> do not move the ball automatically; move it by hand in the gazebo GUI
#   --no-reach -> the iCub only follows the ball with the gaze
#   --show     -> show the camera images with the detected ball
# stop everything with Ctrl+C

demo_dir="$(cd "$(dirname "$0")" && pwd)"
sim_dir="$demo_dir/../../../gz_environment"
logdir="$sim_dir/logs"

sim_args=()
ball_args=()
demo_args=()
for arg in "$@"
do
    case $arg in
        --no-gui) sim_args+=(--no-gui) ;;
        --static) ball_args+=(--static) ;;
        --no-reach|--show) demo_args+=("$arg") ;;
        *) echo "unknown argument: $arg"; exit 1 ;;
    esac
done

pids=()
stop_all() {
    trap - INT TERM
    echo "stop the red ball demo"
    # stop the python scripts first (ball, arms), then the simulation
    # (background processes ignore SIGINT, so SIGTERM is used; the scripts handle it like Ctrl+C)
    kill -TERM "${pids[@]:1}" 2>/dev/null
    sleep 3
    kill -TERM "${pids[0]}" 2>/dev/null
    wait "${pids[0]}"
    exit
}
trap stop_all INT TERM

#### start the simulation; start_all.sh waits until everything is ready
rm -f "$logdir/cartesian_controller.log"    # the log of a previous run would fulfill the wait condition below
bash "$sim_dir/start_all.sh" "${sim_args[@]}" &
pids+=($!)

printf "wait for the simulation "
# the cartesian solvers are started last by start_all.sh
until grep -q "cartesianSolver/left_arm is alive... ready" "$logdir/cartesian_controller.log" 2>/dev/null \
    && grep -q "cartesianSolver/right_arm is alive... ready" "$logdir/cartesian_controller.log" 2>/dev/null
do
    if ! kill -0 "${pids[0]}" 2>/dev/null
    then
        echo "failed, see $logdir"
        exit 1
    fi
    sleep 1
done
echo "ok"

#### start the moving ball and the demo
cd "$demo_dir"
python move_ball.py "${ball_args[@]}" > "$logdir/redball_ball.log" 2>&1 &
pids+=($!)
python redball_demo.py "${demo_args[@]}" &
pids+=($!)

wait
