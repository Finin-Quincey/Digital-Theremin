"""
Ultrasonic Rangefinder

This module provides a class representing an ultrasonic rangefinder.
"""

from machine import Pin
import utime

SPEED_OF_SOUND = 0.343  # Speed of sound in air, in mm/us
PULSE_LENGTH = 10       # Length of pulse sent from trig pin, in us

class USRangefinder:

    def __init__(self, trig, echo):
        self._pin_trig = Pin(trig, Pin.OUT)
        self._pin_echo = Pin(echo, Pin.IN)

    def read(self):

        # Pulse trig pin high
        self._pin_trig.high()
        utime.sleep_us(PULSE_LENGTH)
        self._pin_trig.low()

        on = 0
        off = 0

        while self._pin_echo.value() == 0:
            off = utime.ticks_us()

        while self._pin_echo.value() == 1:
            on = utime.ticks_us()

        elapsed = on - off
        if elapsed > 5000: return -1 # Out of range
        dist = (elapsed * SPEED_OF_SOUND) / 2 # Divide by 2 to account for outward and return trips

        return dist