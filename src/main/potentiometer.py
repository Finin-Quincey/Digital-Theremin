"""
Potentiometer

This module provides a class representing a standard 3-pin potentiometer.
"""

from machine import Pin, ADC

class Potentiometer:

    def __init__(self, pin):
        self._pin = ADC(Pin(pin))

    def read(self):
        # TODO: Decide whether to normalise this here or outside the class
        return self._pin.read_u16()