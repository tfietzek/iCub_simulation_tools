"""
Red ball demo: spawn a red ball in the gz sim world and move it around in front of the iCub.

The ball moves along waypoints given in the iCub root frame (x backwards, y to the right, z upwards).
Some waypoints are within reach of the arms (the iCub reaches for the ball), others are only
in the field of view (the iCub only follows the ball with the gaze).

usage: python move_ball.py (--static)
    --static -> place the ball only once in front of the robot; move it by hand in the gazebo GUI
"""

import os
import signal
import sys
import time

import numpy as np

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../python_scripts"))
import Python_libraries.gz_world_controller as gz_ctrl

BALL_RADIUS = 0.03          # m
BALL_COLOR = [255, 0, 0]    # RGB
SPEED = 0.05                # m/s between the waypoints
PAUSE = 5.0                 # s, how long the ball stays at a waypoint

# waypoints in the iCub root frame [x, y, z] in m
WAYPOINTS_ROBOT = [
    [-0.55, 0.00, 0.20],    # far in front    -> only gaze
    [-0.28, 0.15, 0.05],    # right, in reach -> right arm
    [-0.55, 0.25, 0.25],    # far right       -> only gaze
    [-0.28, -0.15, 0.05],   # left, in reach  -> left arm
    [-0.55, -0.25, 0.10],   # far left        -> only gaze
]


# iCub root frame -> gz sim world frame; the iCub model (iCubGazeboV2_5_visuomanip) is placed at z = 0.63 m,
# rotated by 180 deg around z (Transfermat_robot2gazebo of the Python_libraries uses z = 0.6 m)
T_ROBOT2WORLD = np.array([[-1., 0., 0., 0.],
                          [0., -1., 0., 0.],
                          [0., 0., 1., 0.63],
                          [0., 0., 0., 1.]])


def robot2world(pos_robot):
    """Transform a position from the iCub root frame to the gazebo world frame."""
    pos = np.append(np.array(pos_robot, dtype=float), 1.)
    return (T_ROBOT2WORLD @ pos)[:3].tolist()


def main():
    # handle SIGTERM (e.g. from start_redball.sh) like Ctrl+C
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    static = "--static" in sys.argv[1:]

    world = gz_ctrl.WorldController()
    waypoints = [np.array(robot2world(p)) for p in WAYPOINTS_ROBOT]

    ball = world.create_object("sphere", [BALL_RADIUS], waypoints[0].tolist(), [0, 0, 0], BALL_COLOR,
                               gravity=False, collision=False)
    if not ball:
        sys.exit("Could not create the ball!")
    print("created ball:", ball)

    try:
        if static:
            print("ball placed, move it in the gazebo GUI; stop with Ctrl+C")
            while True:
                time.sleep(1.)

        print("move the ball along the waypoints; stop with Ctrl+C")
        dt = 0.05
        idx = 0
        while True:
            start, goal = waypoints[idx], waypoints[(idx + 1) % len(waypoints)]
            steps = max(1, int(np.linalg.norm(goal - start) / SPEED / dt))
            for s in range(1, steps + 1):
                # smooth start and stop of the motion
                a = 0.5 - 0.5 * np.cos(np.pi * s / steps)
                world.set_pose(ball, (start + a * (goal - start)).tolist(), [0, 0, 0])
                time.sleep(dt)
            idx = (idx + 1) % len(waypoints)
            time.sleep(PAUSE)
    except KeyboardInterrupt:
        pass
    finally:
        world.close()


if __name__ == '__main__':
    main()
