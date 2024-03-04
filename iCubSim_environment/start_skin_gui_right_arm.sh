
#### start skin gui
echo "start skin gui for right arm"
xterm -e 'iCubSkinGui --from right_arm.ini; bash' &
sleep 6

#### connect gui with simulator
xterm -e 'yarp connect /icubSim/skin/right_arm_comp /skinGui/right_arm:i;sleep 0.5; exit; bash' &
echo "started right eye viewer" 
