"""
Red ball demo for the gz sim iCub (inspired by the demoRedBall of icub-main)

The iCub detects a red ball in both eye cameras, follows it with the gaze and reaches for it
with the closer arm (cartesian controller), if the ball is within reach.
If the ball leaves the reachable space, the arm returns to its start pose.

The gaze is controlled by head_gaze.HeadGaze (position control of the head with the iKin eye kinematics),
since iKinGazeCtrl does not work with gz sim yet (see head_gaze.py).

Requirements (see ReadMe.md):
    - simulation with cartesian controller: bash gz_environment/start_all.sh
    - a red ball in the world, e.g.: python move_ball.py

usage: python redball_demo.py (--no-reach) (--show)
    --no-reach -> only follow the ball with the gaze
    --show     -> show the camera images with the detected ball (OpenCV window)
"""

import collections
import signal
import sys
import time

import cv2
import numpy as np
import yarp

from head_gaze import HeadGaze

CLIENT_PREFIX = "/redball"
ROBOT_PREFIX = "/icubSim"
IMG_W, IMG_H = 320, 240

# red color detection in HSV space (OpenCV: H in [0, 180])
# the arm covers of the iCub model are red too, but less saturated (S <= ~150) than the ball (S = 255)
HSV_LOWER = [(0, 200, 60), (170, 200, 60)]
HSV_UPPER = [(10, 255, 255), (180, 255, 255)]
MIN_AREA = 15               # px, smaller blobs are ignored

# gaze
STILL_FRAMES = 3            # the head has to be still for this many frames, before the images are used
CENTER_TOL = 8              # px, the gaze is only moved, if the ball is further away from the image center
MAX_RAY_DIST = 0.02         # m, max. distance of the two eye rays for a valid triangulation
MONO_DISTANCE = 0.5         # m, assumed ball distance, if the ball is only visible in one eye
LOST_TIMEOUT = 3.0          # s without ball -> look at the home position
HOME_FIXATION = [-0.5, 0., 0.1]

# reachable space in the iCub root frame (x backwards, y to the right, z upwards) in m
REACH_X = (-0.38, -0.18)
REACH_Y = 0.35              # |y| <= REACH_Y
REACH_Z = (-0.10, 0.25)
REACH_OFFSET = np.array([0.06, 0., 0.])     # stop the hand in front of the ball (towards the robot)
STABLE_POINTS = 5           # the ball position has to be stable for this many measurements before reaching
STABLE_TOL = 0.02           # m


######################################################################
# helpers for YARP
def to_yarp(values):
    vec = yarp.Vector(len(values))
    for i, v in enumerate(values):
        vec.set(i, float(v))
    return vec


class EyeCamera:
    """Buffered input port for one eye camera; read() returns the newest image as RGB numpy array."""

    def __init__(self, side):
        self.port = yarp.BufferedPortImageRgb()
        local = f"{CLIENT_PREFIX}/cam/{side}:i"
        if not self.port.open(local):
            sys.exit(f"[ERROR] Could not open port {local}")
        # name of the camera port in gz sim; fallback to the old name
        if not (yarp.Network.connect(f"{ROBOT_PREFIX}/cam/{side}/rgbImage:o", local)
                or yarp.Network.connect(f"{ROBOT_PREFIX}/cam/{side}", local)):
            sys.exit(f"[ERROR] Could not connect the {side} camera")

        self.array = np.zeros((IMG_H, IMG_W, 3), dtype=np.uint8)
        self.image = yarp.ImageRgb()
        self.image.resize(IMG_W, IMG_H)
        self.image.setExternal(self.array.data, IMG_W, IMG_H)

    def read(self):
        img = self.port.read(True)
        if img is None:
            return None
        if img.width() != IMG_W or img.height() != IMG_H:
            sys.exit(f"[ERROR] Unexpected image size {img.width()}x{img.height()}")
        self.image.copy(img)
        return self.array

    def close(self):
        self.port.close()


######################################################################
# perception
def detect_ball(rgb):
    """Return the pixel position [u, v] of the biggest red blob and the mask; None if there is no ball."""
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    mask = np.zeros(hsv.shape[:2], dtype=np.uint8)
    for lower, upper in zip(HSV_LOWER, HSV_UPPER):
        mask |= cv2.inRange(hsv, np.array(lower), np.array(upper))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

    n, _, stats, centroids = cv2.connectedComponentsWithStats(mask)
    if n <= 1:
        return None, mask
    biggest = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
    if stats[biggest, cv2.CC_STAT_AREA] < MIN_AREA:
        return None, mask
    return centroids[biggest], mask


def show(images, pixels):
    views = []
    for rgb, px in zip(images, pixels):
        bgr = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)
        if px is not None:
            cv2.circle(bgr, (int(px[0]), int(px[1])), 8, (0, 255, 0), 2)
        views.append(bgr)
    cv2.imshow("redball: left | right", np.hstack(views))
    cv2.waitKey(1)


######################################################################
# reaching
class Arm:
    def __init__(self, part):
        self.part = part
        prop = yarp.Property()
        prop.put("device", "cartesiancontrollerclient")
        prop.put("remote", f"{ROBOT_PREFIX}/cartesianController/{part}")
        prop.put("local", f"{CLIENT_PREFIX}/{part}")
        self.driver = yarp.PolyDriver(prop)
        if not self.driver.isValid():
            sys.exit(f"[ERROR] Could not open the cartesian controller {part}; is it running? "
                     "(bash gz_environment/start_all.sh)")
        self.cart = self.driver.viewICartesianControl()
        self.cart.setTrajTime(1.5)
        pos, orient = yarp.Vector(3), yarp.Vector(4)
        self.cart.getPose(pos, orient)
        self.home = (pos, orient)
        self.reaching = False

    def reach(self, target):
        self.cart.goToPosition(to_yarp(target))
        self.reaching = True

    def go_home(self):
        if self.reaching:
            self.cart.goToPose(*self.home)
            self.reaching = False

    def close(self):
        if self.reaching:
            self.go_home()
            self.cart.waitMotionDone(0.1, 5.0)
        self.cart.stopControl()
        self.driver.close()


def in_reach(point):
    return (REACH_X[0] <= point[0] <= REACH_X[1] and abs(point[1]) <= REACH_Y
            and REACH_Z[0] <= point[2] <= REACH_Z[1])


######################################################################
def main():
    # handle SIGTERM (e.g. from start_redball.sh) like Ctrl+C
    signal.signal(signal.SIGTERM, signal.default_int_handler)
    args = sys.argv[1:]
    reach_enabled = "--no-reach" not in args
    show_images = "--show" in args

    yarp.Network.init()
    if not yarp.Network.checkNetwork():
        sys.exit("[ERROR] Please try running yarp server")

    cams = [EyeCamera("left"), EyeCamera("right")]
    try:
        gaze = HeadGaze(ROBOT_PREFIX, CLIENT_PREFIX)
    except RuntimeError as err:
        sys.exit(f"[ERROR] {err}; is the simulation running?")

    arms = {}
    if reach_enabled:
        arms = {"right_arm": Arm("right_arm"), "left_arm": Arm("left_arm")}

    history = collections.deque(maxlen=STABLE_POINTS)
    last_seen = time.time()
    last_distance = MONO_DISTANCE
    still_count = 0
    looking_home = False
    gaze.look_at(HOME_FIXATION)
    print("redball demo is running; stop with Ctrl+C")

    try:
        while True:
            images = [cam.read() for cam in cams]
            if any(img is None for img in images):
                continue
            pixels = [detect_ball(img)[0] for img in images]
            if show_images:
                show(images, pixels)

            # the camera images lag behind the joint encoders -> use the images only with a still head
            still_count = still_count + 1 if gaze.is_still() else 0
            px_l, px_r = pixels

            if px_l is None and px_r is None:
                history.clear()
                if time.time() - last_seen > LOST_TIMEOUT and not looking_home:
                    print("ball lost -> look at home position")
                    gaze.look_at(HOME_FIXATION)
                    for arm in arms.values():
                        arm.go_home()
                    looking_home = True
                continue
            last_seen = time.time()
            looking_home = False

            if still_count < STILL_FRAMES:
                continue
            q = gaze.get_joints()
            # follow the ball with the gaze
            if px_l is not None and px_r is not None:
                ball, ray_dist = gaze.triangulate(px_l, px_r, q)
                if ball is None or ray_dist > MAX_RAY_DIST:
                    continue
                # distance from the left eye; used, if the ball is only visible in one eye
                last_distance = np.linalg.norm(ball - gaze.eye_pose("left", q)[:3, 3])
                history.append(ball)
            else:
                side, px = ("left", px_l) if px_l is not None else ("right", px_r)
                ball = gaze.mono_point(side, px, last_distance, q)
                history.clear()

            offset = max(np.max(np.abs(np.asarray(px) - [IMG_W / 2., IMG_H / 2.]))
                         for px in pixels if px is not None)
            if offset > CENTER_TOL:
                gaze.look_at(ball)
                still_count = 0

            if not arms or len(history) < STABLE_POINTS:
                continue

            # reach for the ball, if its position is stable and reachable
            points = np.array(history)
            ball = points.mean(axis=0)
            if np.max(np.linalg.norm(points - ball, axis=1)) > STABLE_TOL:
                continue

            if in_reach(ball):
                part = "right_arm" if ball[1] > 0 else "left_arm"
                if not arms[part].reaching:
                    print(f"ball at {np.round(ball, 3)} -> reach with {part}")
                arms[part].reach(ball + REACH_OFFSET)
                for other, arm in arms.items():
                    if other != part:
                        arm.go_home()
            else:
                if any(arm.reaching for arm in arms.values()):
                    print(f"ball at {np.round(ball, 3)} out of reach -> arms home")
                for arm in arms.values():
                    arm.go_home()
    except KeyboardInterrupt:
        pass
    finally:
        print("close the demo")
        for arm in arms.values():
            arm.close()
        gaze.close()
        for cam in cams:
            cam.close()
        if show_images:
            cv2.destroyAllWindows()
        yarp.Network.fini()


if __name__ == '__main__':
    main()
