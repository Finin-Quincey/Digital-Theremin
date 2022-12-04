"""
Main digital theremin script
"""

import _thread
import utime
import math

from potentiometer import Potentiometer
from ultrasound_sensor import USRangefinder
from pio_dac import PIOPWM

from machine import Pin

led_pin = Pin(25, Pin.OUT)
led_pin.high()

stop_btn = Pin(13, Pin.IN, pull = Pin.PULL_UP)

# The basic idea here is that rather than changing the sampling rate (as in the sine example),
# we have a fixed sampling frequency (which is really just as fast as possible) and we take
# samples from the waveform as necessary to convert it to the desired frequency

# We seem to be able to change the PWM at roughly 20kHz maximum, so that's our sampling frequency

SAMPLE_LEN = 5000
AMPLITUDE = 128

PITCH_AVG_WINDOW = 2

pwm = PIOPWM(0, 14, max_count=250, count_freq=10_000_000)

#waveform = bytearray(int(n/SAMPLE_LEN * AMPLITUDE) for n in range(SAMPLE_LEN)) # Sawtooth
waveform = bytearray(int((math.sin(2 * math.pi * t/SAMPLE_LEN) + 1)/2 * AMPLITUDE) for t in range(int(SAMPLE_LEN))) # Sine

prev_pitch = [255] * PITCH_AVG_WINDOW

vol = 255
pitch = 255

### Input read thread ###

def read_pot():
    global vol, pitch, stop_btn, prev_pitch
    vol_ctrl = USRangefinder(17, 18)
    pitch_ctrl = USRangefinder(15, 16)
    while stop_btn.value():
        vol = max(255 - int(vol_ctrl.read()), 0)
        p   = min(int(pitch_ctrl.read()), 255)
        prev_pitch.insert(0, p)
        prev_pitch = prev_pitch[:PITCH_AVG_WINDOW]
        pitch = sum(prev_pitch) // PITCH_AVG_WINDOW
        #if utime.ticks_ms() % 1000 < 20: print(utime.ticks_ms())
        utime.sleep_ms(1)

_thread.start_new_thread(read_pot, ())

### Audio output thread ###

while stop_btn.value():
    for i in range(0, 255):
        pwm.set((vol * waveform[(i * pitch * 2) % SAMPLE_LEN]) // 255)