maxPwm = 12.0
minPwm = 2.0
midPwm = round( (maxPwm+minPwm) / 2 , 0 )

flEnginePin=37
frEnginePin=33
rlEnginePin=35
rrEnginePin=40

leftXAxisIgnoreRange = range(119, 136)
leftYAxisIgnoreRange = range(124, 131)
rightXAxisIgnoreRange = range(122, 132)
rightYAxisIgnoreRange = range(125, 130)

# Horizontal camera movement (right-left)
panServoPin=36
panMinPwm=2.0
panMaxPwm=12.0

# Vertical camera movement (up-down)
tiltServoPin=38
tiltMinPwm=5.0
tiltMaxPwm=10.0