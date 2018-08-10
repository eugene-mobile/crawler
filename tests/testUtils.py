import unittest
import utils
import constants

class TestMethods(unittest.TestCase):

    def testCalculateSpeedPwm(self):
        result = utils.calculateSpeedPwm(255)
        self.assertEqual(constants.maxPwm, result, "Joystick in bottom position should attribute to maximum reverse")

        result = utils.calculateSpeedPwm(0)
        self.assertEqual(constants.minPwm, result, "Joystick in top position should attribute to maximum forward")

        result = utils.calculateSpeedPwm(127)
        text = "Joystick in around neutral position {} should attribute to engine stop pwm".format(127)
        self.assertEqual( (constants.maxPwm-constants.minPwm)/2 + constants.minPwm, result, text)

    def testSpeedChangeGradual(self):
        lastPwm = constants.minPwm
        for position in range(0, 256):
            newPwm = utils.calculateSpeedPwm(position)
            msg = "Joystick position change from {} to {} caused too big PWM change: from {} to {}".format(position-1, position, lastPwm, newPwm)
            self.assertAlmostEqual(newPwm, lastPwm, delta=0.11, msg=msg)
            lastPwm = newPwm

    def testCalculateSteeringPwmAdjustment(self):
        for position in range(0, 4):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, -2, "PWM change for joystick in left position at {} should be -2".format(position))

        for position in range(4, 10):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, -1.9, "PWM change for joystick in left position at {} should be -1.9".format(position))


        for position in range(32, 36):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, -1.5, "PWM change for joystick in left position at {} should be -1.5".format(position))


        for position in range(96, 99):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, -0.5, "PWM change for joystick in left position at {} should be -0.5".format(position))

        for position in range(120, 125):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, -0.1, "PWM change for joystick in left position at {} should be -0.1".format(position))    

        for position in range(125, 131):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, 0, "PWM change for joystick in left position at {} should be 0".format(position))    
        
        result = utils.calculateSteeringPwmAdjustment(131)
        self.assertEqual(result, 0.1, "PWM change for joystick in left position at 131 should be 0.1")    


        for position in range(160, 163):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, 0.5, "PWM change for joystick in left position at {} should be 1".format(position))
        
        for position in range(252, 256):
            result = utils.calculateSteeringPwmAdjustment(position)
            self.assertEqual(result, 2, "PWM change for joystick in left position at {} should be 2".format(position))

    def testSteerichChangeGradual(self):
        lastPwm = -2.0
        for position in range(0, 256):
            newPwm = utils.calculateSteeringPwmAdjustment(position)
            msg = "Joystick X position change from {} to {} caused too big PWM change: from {} to {}".format(position-1, position, lastPwm, newPwm)
            self.assertAlmostEqual(newPwm, lastPwm, delta=0.11, msg=msg)
            lastPwm = newPwm

    def testCalculateMaxTilt(self):
        result = utils.calculateTiltPwm(255)
        self.assertAlmostEqual(constants.tiltMaxPwm, result, 0.1)

    def testCalculateMinTilt(self):
        result = utils.calculateTiltPwm(0)
        self.assertAlmostEqual(constants.tiltMinPwm, result, 0.1)

    def testCalculateMidTilt(self):
        result = utils.calculateTiltPwm(255/2)
        self.assertAlmostEqual( (constants.maxPwm+constants.minPwm)/2, result, 0.1)

    def testCalculateMaxPan(self):
        result = utils.calculatePanPwm(255)
        self.assertAlmostEqual(constants.panMaxPwm, result, 0.1)

    def testCalculateMinPan(self):
        result = utils.calculatePanPwm(0)
        self.assertAlmostEqual(constants.panMinPwm, result, 0.1)

    def testCalculateMidPan(self):
        result = utils.calculatePanPwm(255/2)
        self.assertAlmostEqual( (constants.maxPwm+constants.minPwm)/2, result, 0.1)


if __name__ == '__main__':
    unittest.main()