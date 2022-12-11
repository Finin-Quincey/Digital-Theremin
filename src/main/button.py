"""
Button

This module provides a class representing a button.
"""

from machine import Pin
import utime

DEBOUNCE_WINDOW = 20 # Debounce window in ms

class Button:

    def __init__(self, pin):
        self._pin = Pin(pin, Pin.IN, Pin.PULL_UP)
        self._last_change_time = utime.ticks_ms()
        self._prev_value = 0

    def just_pressed(self):
        v = self._prev_value
        return self.read() and not v

    def read(self):
        if utime.ticks_ms() - self._last_change_time < DEBOUNCE_WINDOW: return self._prev_value
        val = not self._pin.value()
        self._prev_value = val
        return val