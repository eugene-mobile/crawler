import constants
import math

def calculateSpeedPwm(value):
    # value = 255 - value
    # y=((x/(255/(12-2)))+2)
    # speed = round( (value / (255/ (constants.maxPwm-constants.minPwm)))+constants.minPwm, 1)
    
    # y=((x/(255/(12-2)))+2)+sin(x*2*pi/255)
    speed = round( (value / (255/ (constants.maxPwm-constants.minPwm)))+constants.minPwm+math.sin(value*2*math.pi/255), 1)

    speed = max(speed, constants.minPwm)
    speed = min(speed, constants.maxPwm)
    return speed

def calculateSteeringPwmAdjustment(value):
    speed = round( (value / (255/ 4)) - 2, 1)
    speed = max(speed, -2)
    speed = min(speed, 2)
    return speed

def calculatePanPwm(value):
    pwm = round( (value / (255/ (constants.maxPwm-constants.minPwm)))+constants.minPwm, 1)
    pwm = max(pwm, constants.panMinPwm)
    pwm = min(pwm, constants.panMaxPwm)
    return pwm

def calculateTiltPwm(value):
    pwm = round( (value / (255/ (constants.maxPwm-constants.minPwm)))+constants.minPwm, 1)
    pwm = max(pwm, constants.tiltMinPwm)
    pwm = min(pwm, constants.tiltMaxPwm)
    return pwm