

#### start skin gui
echo "start skin gui for right arm"
xterm -e 'iCubSkinGui --from right_hand.ini; bash' &
sleep 6

#### connect gui with simulator
xterm -e 'yarp connect /icubSim/skin/right_hand_comp /skinGui/right_hand:i;sleep 0.5; exit; bash' &
echo "started right eye viewer" 
