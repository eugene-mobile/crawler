import RPi.GPIO as GPIO
import time
import argparse
import evdev
import utils
import constants

parser = argparse.ArgumentParser()
parser.add_argument("--init", help="include ESC initialization sequence")
args = parser.parse_args()

GPIO.setmode(GPIO.BOARD)

GPIO.setup(constants.flEnginePin, GPIO.OUT)
GPIO.setup(constants.frEnginePin, GPIO.OUT)
GPIO.setup(constants.rlEnginePin, GPIO.OUT)
GPIO.setup(constants.rrEnginePin, GPIO.OUT)
GPIO.setup(constants.panServoPin, GPIO.OUT)
GPIO.setup(constants.tiltServoPin, GPIO.OUT)

flEngine = GPIO.PWM(constants.flEnginePin, 50)
frEngine = GPIO.PWM(constants.frEnginePin, 50)
rlEngine = GPIO.PWM(constants.rlEnginePin, 50)
rrEngine = GPIO.PWM(constants.rrEnginePin, 50)
pan = GPIO.PWM(constants.panServoPin, 50)
tilt = GPIO.PWM(constants.tiltServoPin, 50)

def initESC(pin):
    pin.start(constants.minPwm)
    time.sleep(0.1)
    pin.ChangeDutyCycle(constants.maxPwm)
    time.sleep(0.1)
    pin.ChangeDutyCycle(constants.minPwm)
    time.sleep(0.1)
    pin.ChangeDutyCycle( constants.midPwm )
    time.sleep(0.1)

def throttle(pin, value):
    pin.ChangeDutyCycle(value)

def stop():
    flEngine.ChangeDutyCycle( constants.midPwm )
    frEngine.ChangeDutyCycle( constants.midPwm )
    rlEngine.ChangeDutyCycle( constants.midPwm )
    rrEngine.ChangeDutyCycle( constants.midPwm )

def setSpeed(speed, sleepTime):
    throttle(flEngine, speed)
    throttle(frEngine, speed)
    throttle(rlEngine, speed)
    throttle(rrEngine, speed)
    time.sleep(sleepTime)

def setEnginesSpeed(speed, steeringAdjustment):
    throttle(flEngine, speed+steeringAdjustment)
    throttle(frEngine, speed-steeringAdjustment)
    throttle(rlEngine, speed+steeringAdjustment)
    throttle(rrEngine, speed-steeringAdjustment)

def forward(speed, sleepTime):
    setSpeed( constants.midPwm+speed, sleepTime)
    stop()

def reverse(speed, sleepTime):
    setSpeed(speed, sleepTime)
    stop()

if args.init:
    initESC(frEngine)
    initESC(flEngine)
    initESC(rrEngine)
    initESC(rlEngine)
    initESC(pan)
    initESC(tilt)
    pan.start(constants.midPwm)
    tilt.start(constants.midPwm)
else:    
    frEngine.start(constants.midPwm)
    flEngine.start(constants.midPwm)
    rrEngine.start(constants.midPwm)
    rlEngine.start(constants.midPwm)
    pan.start(constants.midPwm)
    tilt.start(constants.midPwm)


devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
    print( device.path, device.name, device.phys)
    if device.name == 'Wireless Controller':
        print('Device is selected as input: ')
        print(device.name, device.phys)
        ps3dev = device.fn

gamepad = evdev.InputDevice(ps3dev)

speed = 0
running = True

lastPwm = 6
lastSteeringPwmAdjustment = 0
for event in gamepad.read_loop():   #this loops infinitely
    if event.type == 0: 
        continue
    if event.type == 3:
        # axis events
        if event.value > 125 and event.value < 130:
            # do not react on small changes
            continue
        elif event.code == 0:   # left X
            position = event.value
            if (position in constants.leftXAxisIgnoreRange):
                # print("Ignoring left X axis value %s. Setting to %s" % (position, 127))
                position = 127
            pwm = utils.calculateSteeringPwmAdjustment(position)
            if (pwm == lastSteeringPwmAdjustment):
                continue
            print("Left X axis value %s -> Changing speed pwm to %s" % (event.value, pwm))
            lastSteeringPwmAdjustment = pwm
            continue
        elif event.code == 1:   # left Y
            position = event.value
            if (position in constants.leftYAxisIgnoreRange):
                # print("Ignoring left Y axis value %s. Setting to %s" % (position, 127))
                position = 127
            pwm = utils.calculateSpeedPwm(position)
            if (pwm==lastPwm):
                continue
            print("Left Y axis value %s -> Changing speed pwm to %s" % (event.value, pwm))
            lastPwm = pwm
            setEnginesSpeed(pwm, lastSteeringPwmAdjustment)
        elif event.code == 3:   # right X
            position = event.value
            if (position in constants.rightXAxisIgnoreRange):
                position = 127
            pwm = utils.calculatePanPwm(position)
            print("Right X axis value %s -> Changing pan pwm to %s" % (event.value, pwm))
            pan.ChangeDutyCycle(pwm)
            continue
        elif event.code == 4:   # right Y
            position = event.value
            if (position in constants.rightYAxisIgnoreRange):
                position = 127
            pwm = utils.calculateTiltPwm(position)
            print("Right Y axis value %s -> Changing tilt pwm to %s" % (event.value, pwm))
            tilt.ChangeDutyCycle(pwm)
            continue
        else:
            #print("Other axis event ", event)
            continue
    elif event.type == 1: 
        print("Button pressed ", event)
        if event.code == 304 and event.value == 1:
            print("Exiting")
            flEngine.stop()
            frEngine.stop()
            rlEngine.stop()
            rrEngine.stop()
            GPIO.cleanup()
            break
        continue
    else:
        print("Event ", event)