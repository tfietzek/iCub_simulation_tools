## Red ball demo (gz sim)

Python version of the red ball demo of icub-main (`demoRedBall`), which is not part of the conda packages.
The iCub detects a red ball in both eye cameras, follows it with the gaze and reaches for it with the closer arm, if the ball is within reach.
If the ball leaves the reachable space, the arm returns to its start pose.

### Files

- *start_redball.sh (--no-gui) (--static) (--no-reach) (--show)* -> start everything in one terminal: simulation with cartesian controller (`gz_environment/start_all.sh`), the moving ball and the demo; stop with Ctrl+C
  - --no-gui -> gazebo without GUI-client
  - --static -> the ball is not moved automatically; move it by hand in the gazebo GUI
  - --no-reach -> only follow the ball with the gaze
  - --show -> show the camera images with the detected ball
- *redball_demo.py (--no-reach) (--show)* -> the demo: red color detection (OpenCV, HSV threshold), gaze control (head_gaze.py), reaching (cartesian controller)
- *head_gaze.py* -> simple gaze controller for the gz sim iCub: fixation of 3D points with position control of the head, stereo triangulation; uses the iKin eye kinematics of icub-main
- *move_ball.py (--static)* -> spawn a red ball and move it along waypoints in front of the iCub (some in reach, some only in view)

### Manual start

```bash
bash gz_environment/start_all.sh            # terminal 1
python demos/redball/move_ball.py           # terminal 2
python demos/redball/redball_demo.py        # terminal 3
```

### How it works

1. The red ball is detected in both camera images (biggest blob with red hue and high saturation).
2. The head has to be still for some frames, since the camera images lag behind the joint encoders.
3. The 3D ball position is triangulated from the pixels in both eyes and the current head joints (accuracy in the simulation: about 1-15 mm).
4. If the ball is not in the image center, the head fixates the ball: `HeadGaze.solve` computes the head joints (neck pitch/yaw, eye tilt/version/vergence), so that the ball is in the center of both images; the eyes are kept near 0, so that the neck does most of the motion.
5. If the ball position is stable and within reach, the closer arm moves its hand 6 cm in front of the ball.

### Notes

- iKinGazeCtrl is not used, since it does not work with gz sim yet: it controls the eyes in the mixed position/velocity control mode, which the controlboard plugin of gz-sim-yarp-plugins does not implement ([gz-sim-yarp-plugins#144](https://github.com/robotology/gz-sim-yarp-plugins/issues/144)). In addition, the velocity control of the coupled eye joints does not reach the joints and the velocity control of the neck is unstable.
- The arm covers of the iCub model are red too, but less saturated (HSV saturation <= ~150) than the ball (255); therefore the saturation threshold of the detection is 200.
- In the gz sim world the iCub root is at z = 0.63 m (rotated by 180 deg around z); `Transfermat_robot2gazebo` of the Python_libraries uses 0.6 m. `move_ball.py` uses its own transformation.
