"""
Simple gaze controller for the gz sim iCub, using only position control of the head.

iKinGazeCtrl does not work with gz sim yet: it controls the eyes in the mixed position/velocity
control mode, which the controlboard plugin of gz-sim-yarp-plugins does not implement
(https://github.com/robotology/gz-sim-yarp-plugins/issues/144).
This module uses the same iKin eye kinematics (python bindings of icub-main), but commands the
head joints with position control, which works in gz sim.

Head joints: 0 neck_pitch, 1 neck_roll, 2 neck_yaw, 3 eyes_tilt, 4 eyes_version, 5 eyes_vergence
All positions are in the iCub root frame (x backwards, y to the right, z upwards), angles in deg.
"""

import icub
import numpy as np
import yarp

# camera intrinsics of the gz sim iCub eyes (320x240, horizontal fov 50 deg)
CAM_W, CAM_H = 320, 240
CAM_F = 0.5 * CAM_W / np.tan(np.deg2rad(25.))
CAM_K = np.array([[CAM_F, 0., CAM_W / 2.],
                  [0., CAM_F, CAM_H / 2.],
                  [0., 0., 1.]])

NECK_ROLL = 0.          # the neck roll is not used for the gaze
EYE_WEIGHT = 0.05       # regularization: keeps the eyes (tilt, version) near 0 -> the neck does most of the work
STILL_TOL = 0.3         # deg, max. joint change between two calls of is_still() for a still head


class HeadGaze:
    def __init__(self, robot="/icubSim", local="/headgaze", head_version="v2.5"):
        prop = yarp.Property()
        prop.put("device", "remote_controlboard")
        prop.put("remote", robot + "/head")
        prop.put("local", local + "/head")
        self.driver = yarp.PolyDriver(prop)
        if not self.driver.isValid():
            raise RuntimeError("Could not connect to the head controlboard " + robot + "/head")
        self.enc = self.driver.viewIEncoders()
        self.pos = self.driver.viewIPositionControl()
        self.mode = self.driver.viewIControlMode()
        limits = self.driver.viewIControlLimits()

        self.n_joints = self.pos.getAxes()
        self.lim = np.zeros((self.n_joints, 2))
        for j in range(self.n_joints):
            ok, lo_v, hi_v = self._get_limits(limits, j)
            self.lim[j] = [lo_v, hi_v] if ok else [-30., 30.]
        # small margin to the joint limits
        self.lim += np.array([1., -1.])

        for j in range(self.n_joints):
            self.mode.setControlMode(j, yarp.VOCAB_CM_POSITION)
        self.set_speeds(neck=40., eyes=80.)

        # eye kinematics; the torso is not moved by this demo -> torso links stay at 0
        self.eyes = {side: icub.iCubEye(f"{side}_{head_version}") for side in ("left", "right")}
        for eye in self.eyes.values():
            for i in range(3):
                eye.blockLink(i, 0.)
        self._last_q = self.get_joints()

    @staticmethod
    def _get_limits(limits, j):
        # the signature of getLimits differs between YARP versions of the python bindings
        try:
            lo, hi = yarp.DVector(1), yarp.DVector(1)
            ok = limits.getLimits(j, lo, hi)
            return ok, lo[0], hi[0]
        except TypeError:
            res = limits.getLimits(j)
            return res[0], res[1], res[2]

    def set_speeds(self, neck=40., eyes=80.):
        for j in range(self.n_joints):
            self.pos.setRefSpeed(j, neck if j < 3 else eyes)

    ######################################################################
    # kinematics
    def get_joints(self):
        q = yarp.DVector(self.n_joints)
        self.enc.getEncoders(q)
        return np.array(list(q))

    def eye_pose(self, side, q_head):
        """Homogeneous transformation of the eye camera (z: optical axis, x: image u, y: image v) in the root frame."""
        verg = q_head[5] / 2. if side == "left" else -q_head[5] / 2.
        q = [q_head[0], q_head[1], q_head[2], q_head[3], q_head[4] + verg]
        eye = self.eyes[side]
        vec = yarp.Vector(eye.getDOF())
        for i, v in enumerate(q):
            vec.set(i, np.deg2rad(v))
        eye.setAng(vec)
        H = eye.getH()
        return np.array([[H.get(r, c) for c in range(4)] for r in range(4)])

    def project(self, side, q_head, point):
        """Pixel [u, v] of a 3D point in the given eye; None if the point is behind the camera."""
        H = self.eye_pose(side, q_head)
        p = np.linalg.inv(H) @ np.append(point, 1.)
        if p[2] <= 1e-6:
            return None
        uv = CAM_K @ p[:3]
        return uv[:2] / uv[2]

    def pixel_ray(self, side, q_head, pixel):
        """Origin and direction (root frame) of the ray through the pixel of the given eye."""
        H = self.eye_pose(side, q_head)
        d_cam = np.linalg.inv(CAM_K) @ np.array([pixel[0], pixel[1], 1.])
        d = H[:3, :3] @ d_cam
        return H[:3, 3], d / np.linalg.norm(d)

    def triangulate(self, px_left, px_right, q_head=None):
        """3D point from the pixels of the same object in both eyes (midpoint of the closest points of both rays).
           Returns the point and the distance between the rays (quality measure); None if the rays diverge."""
        q_head = self.get_joints() if q_head is None else q_head
        o1, d1 = self.pixel_ray("left", q_head, px_left)
        o2, d2 = self.pixel_ray("right", q_head, px_right)
        w = o1 - o2
        a, b, c, d, e = d1 @ d1, d1 @ d2, d2 @ d2, d1 @ w, d2 @ w
        den = a * c - b * b
        if den < 1e-9:
            return None, None
        s, t = (b * e - c * d) / den, (a * e - b * d) / den
        if s <= 0 or t <= 0:
            return None, None
        p1, p2 = o1 + s * d1, o2 + t * d2
        return (p1 + p2) / 2., np.linalg.norm(p1 - p2)

    def mono_point(self, side, pixel, distance, q_head=None):
        """3D point on the ray through the pixel of one eye at the given distance."""
        q_head = self.get_joints() if q_head is None else q_head
        o, d = self.pixel_ray(side, q_head, pixel)
        return o + distance * d

    ######################################################################
    # gaze
    def solve(self, point, q_start=None, iterations=30):
        """Head joint angles, so that both eyes fixate the 3D point (Gauss-Newton on the pixel errors)."""
        point = np.asarray(point, dtype=float)
        q = (self.get_joints() if q_start is None else np.array(q_start, dtype=float)).copy()
        q[1] = NECK_ROLL
        q[5] = max(q[5], 2.)
        free = [0, 2, 3, 4, 5]
        center = np.array([CAM_W / 2., CAM_H / 2.])

        def residual(qq):
            res = []
            for side in ("left", "right"):
                uv = self.project(side, qq, point)
                if uv is None:
                    return None
                res.extend((uv - center) / CAM_F)
            res.extend([EYE_WEIGHT * np.deg2rad(qq[3]), EYE_WEIGHT * np.deg2rad(qq[4])])
            return np.array(res)

        r = residual(q)
        if r is None:
            return None
        for _ in range(iterations):
            J = np.zeros((len(r), len(free)))
            for k, j in enumerate(free):
                dq = q.copy()
                dq[j] += 0.1
                rd = residual(dq)
                if rd is None:
                    return None
                J[:, k] = (rd - r) / 0.1
            # active set: a joint at its limit, which would be moved further into the limit, is excluded,
            # so that the other joints (e.g. the eyes) take over
            active = np.ones(len(free), dtype=bool)
            for _ in range(len(free)):
                step = np.zeros(len(free))
                step[active] = np.linalg.lstsq(J[:, active], -r, rcond=None)[0]
                new = q[free] + step
                blocked = active & (((new < self.lim[free, 0]) & (q[free] <= self.lim[free, 0] + 1e-6))
                                    | ((new > self.lim[free, 1]) & (q[free] >= self.lim[free, 1] - 1e-6)))
                if not blocked.any():
                    break
                active &= ~blocked
            q[free] = np.clip(q[free] + step, self.lim[free, 0], self.lim[free, 1])
            r_new = residual(q)
            if r_new is None:
                return None
            if np.linalg.norm(r_new - r) < 1e-7:
                r = r_new
                break
            r = r_new
        return q

    def look_at(self, point):
        """Move the head to fixate the 3D point; returns the joint targets or None if there is no solution."""
        q = self.solve(point)
        if q is None:
            return None
        for j in range(self.n_joints):
            self.pos.positionMove(j, float(q[j]))
        return q

    def look_at_angles(self, q):
        for j in range(self.n_joints):
            self.pos.positionMove(j, float(q[j]))

    def is_still(self):
        """True, if the head joints did not move (more than STILL_TOL) since the last call."""
        q = self.get_joints()
        still = np.max(np.abs(q - self._last_q)) < STILL_TOL
        self._last_q = q
        return still

    def fixation_point(self, q_head=None):
        """Current fixation point: intersection of the optical axes of both eyes."""
        c = [CAM_W / 2., CAM_H / 2.]
        return self.triangulate(c, c, q_head)[0]

    def close(self):
        self.driver.close()
