from machine import Pin, PWM, ADC
import utime
import math
from ultrasound_sensor import USRangefinder
from potentiometer import Potentiometer

# Chromatic
#scale = [
#  261.63, # C4
#  277.18, # C#4
#  293.66, # D4
#  311.13, # Eb4
#  329.63, # E4
#  349.23, # F4
#  369.99, # F#4
#  392.00, # G4
#  415.30, # Ab4
#  440.00, # A4
#  466.16, # Bb4
#  493.88, # B4
#  523.25, # C5
#]

# # Major
scale = [
 261.63, # C4
 293.66, # D4
 329.63, # E4
 349.23, # F4
 392.00, # G4
 440.00, # A4
 493.88, # B4
 523.25, # C5
]

# Pentatonic
# scale = [
#  261.63, # C4
#  293.66, # D4
#  329.63, # E4
#  392.00, # G4
#  440.00, # A4
#  523.25, # C5
# ]

# Blues
# scale = [
#   261.63, # C4
#   311.13, # Eb4
#   349.23, # F4
#   369.99, # F#4
#   392.00, # G4
#   466.16, # Bb4
#   523.25, # C5
# ]

# Eastern
# scale = [
#  261.63, # C4
#  277.18, # C#4
#  329.63, # E4
#  349.23, # F4
#  392.00, # G4
#  415.30, # Ab4
#  493.88, # B4
#  523.25, # C5
# ]

led_pin = Pin(25, Pin.OUT)
led_pin.high()

audio_pin = PWM(Pin(18, Pin.OUT))
audio_pin.duty_u16(32767)
audio_pin.freq(440)

vol_ctrl_pin = PWM(Pin(17, Pin.OUT))
vol_ctrl_pin.duty_u16(65535)
vol_ctrl_pin.freq(30000) # Above hearing range so we don't introduce audible noise

vol_ctrl = USRangefinder(7, 9)
pitch_ctrl = USRangefinder(26, 22)

amp_dial = Potentiometer(28)

prev_pitch = [100] * 51

def median(a):
    a_copy = a.copy()
    a_copy.sort()
    return (a_copy[len(a)//2] + a_copy[len(a)//2+1])/2 if len(a) % 2 == 0 else a_copy[len(a)//2]

while True:

    # vol_ctrl_pin.duty_u16(int((math.sin(utime.ticks_ms()/1000) + 1) * 65535))
    # audio_pin.freq(int(100 + (math.sin(utime.ticks_ms()/3300) + 1) * 1000))

    vol   = vol_ctrl.read()
    pitch = pitch_ctrl.read()

    if vol == -1: vol = 330

    amp = amp_dial.read()/65535

    duty = 0 if pitch == -1 else int(min(max(vol * 200, 0), 65535) * amp)

    vol_ctrl_pin.duty_u16(duty)

    # prev_pitch.insert(0, pitch_ctrl.read())
    # prev_pitch = prev_pitch[0:20]
    # audio_pin.freq(int(median(prev_pitch) * 4))
    audio_pin.freq(int(scale[min(int(pitch / 50), len(scale)-1) - 1]))