"""
Main digital theremin script
"""

from machine import Pin, PWM
import utime
import math
from ultrasound_sensor import USRangefinder
from potentiometer import Potentiometer
from button import Button
import scales
import tunes

### Constants ###

VOLUME_SENSITIVITY = 0.005
VOLUME_OFFSET = 35 # How far from the volume sensor the 'zero' point should be, in mm
PITCH_SENSITIVITY = 0.025
PITCH_OFFSET = 35 # How far from the pitch sensor the 'zero' point should be, in mm
START_OCTAVE = 4
WINDOW_SIZE = 7
PORT_THRESHOLD = 2
BTN_HOLD_TIME = 2000


### Classes ###

class Setting:

    def __init__(self, starting_val, min, max, step, wrap = False):
        self.value = starting_val
        self._starting_val = starting_val
        self._min = min
        self._max = max
        self._step = step
        self._wrap = wrap

    def reset(self):
        self.value = self._starting_val

    def increment(self):
        if self.value < self._max:
            self.value += self._step
        elif self._wrap:
            self.value = self._min

    def decrement(self):
        if self.value > self._min:
            self.value -= self._step
        elif self._wrap:
            self.value = self._max


### Setup ###

# Pin definitions
led_pin = Pin(25, Pin.OUT)
led_pin.high()

audio_pin = PWM(Pin(18, Pin.OUT))
audio_pin.duty_u16(32767)
audio_pin.freq(440)

vol_ctrl_pin = PWM(Pin(17, Pin.OUT))
vol_ctrl_pin.duty_u16(65535)
vol_ctrl_pin.freq(30000) # Above hearing range so we don't introduce audible noise

plus_btn  = Button(11)
minus_btn = Button(15)
func_btn  = Button(20)

# Objects
vol_ctrl   = USRangefinder(7, 9)
pitch_ctrl = USRangefinder(26, 22)
amp_dial   = Potentiometer(28)

transpose  = Setting(0, -48, 48, 1)
scale      = Setting(0, 0, len(scales.SCALES)-1, 1, True)
portamento = Setting(100, 0, 1000, 100)

functions = [transpose, scale, portamento]

# Global variables
freq_window = [440.0] * WINDOW_SIZE
func_index = 0
prev_freq = 440
port_start_time = 0
func_btn_hold_start = None


### Functions ###

def median(a):
    a_copy = a.copy()
    a_copy.sort()
    return (a_copy[len(a)//2] + a_copy[len(a)//2+1])/2 if len(a) % 2 == 0 else a_copy[len(a)//2]


def play_tune(tune, tempo):
    """
    Plays a tune at the given tempo in bpm. The tune should be a sequence of tuples, each consisting of a string
    identifying the note name (see `scales.get_note_freq()`) and a duration in beats (fractions are allowed).
    Rests may be specified by leaving the note name blank.
    """
    beat_duration = 60/tempo

    for note in tune:

        note_name = note[0]
        if note_name:
            vol_ctrl_pin.duty_u16(65535)
            audio_pin.freq(int(scales.get_note_freq(note_name)))
        else:
            vol_ctrl_pin.duty_u16(0)

        duration = note[1] * beat_duration
        utime.sleep(duration)

    vol_ctrl_pin.duty_u16(0)
    utime.sleep(2)


### Main program loop ###

while True:

    vol   = vol_ctrl.read()
    pitch = pitch_ctrl.read()
    amp   = amp_dial.read() / 65535

    if vol < 0: vol = 330 # Max volume

    # Perceived volume is not linear!
    vol_linear = min(max((vol - VOLUME_OFFSET) * VOLUME_SENSITIVITY, 0), 1) * amp # 0 to 1
    # 10**0 = 1 so subtract 1 to make it start at 0
    # 10**1 = 10 so divide by 10 to make it 0 to 1 again, except we already subtracted 1 so divide by 9 instead
    vol_exp = (10 ** vol_linear - 1) / 9

    # Calculate duty cycle for volume out (volume is zero if nothing is in front of pitch sensor)
    duty = 0 if pitch < 0 else int(min(max(vol_exp * 65535, 0), 65535))
    vol_ctrl_pin.duty_u16(duty)

    current_scale = scales.SCALES[scale.value]
    scale_len = len(current_scale)

    # Convert to degree of the scale (fractions allowed)
    degree = int(max(0, pitch - PITCH_OFFSET) * PITCH_SENSITIVITY)

    note = (degree // scale_len) * 12 + current_scale[degree % scale_len] + transpose.value

    current_freq = scales.compute_note_freq(START_OCTAVE + note // 12, note % 12)

    # Smoothing
    freq_window.insert(0, current_freq)
    freq_window = freq_window[0:WINDOW_SIZE]

    freq = median(freq_window)

    # Portamento

    if portamento.value > 0:

        port_progress = (utime.ticks_ms() - port_start_time) / portamento.value

        if port_progress < 1:
            freq = prev_freq + (freq - prev_freq) * port_progress
        else:
            if abs(prev_freq - freq) > PORT_THRESHOLD:
                port_start_time = utime.ticks_ms()
            prev_freq = freq

    # Actually set the frequency
    audio_pin.freq(int(freq))

    # Update controls
    flash = False

    if func_btn.just_pressed():
        func_index = (func_index + 1) % len(functions)
        led_pin.low()
        flash = True
    
    if plus_btn.just_pressed(): 
        functions[func_index].increment()
        led_pin.low()
        flash = True

    if minus_btn.just_pressed():
        functions[func_index].decrement()
        led_pin.low()
        flash = True

    if func_btn.read():
        if not func_btn_hold_start:
            func_btn_hold_start = utime.ticks_ms()
        elif utime.ticks_ms() - func_btn_hold_start > BTN_HOLD_TIME:
            play_tune(tunes.CHRISTMAS, 180) # Easter eggs at christmas, very festive
            func_btn_hold_start = None
    else:
        func_btn_hold_start = None

    if plus_btn.read() and minus_btn.read():
        if func_btn.read():
            play_tune(tunes.RICK, 120)
        else:
            functions[func_index].reset()
        led_pin.low()
        flash = True

    if not flash: led_pin.high()
    