from machine import Pin, PWM, ADC
import utime
import math

led_pin = Pin(25, Pin.OUT)
led_pin.high()

audio_pin = PWM(Pin(14, Pin.OUT))
audio_pin.duty_u16(32767)

audio_pin.freq(int(100e6))

pot_pin = ADC(Pin(26))

freq = 440

trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(16, Pin.PULL_DOWN)

WINDOW_LEN = 20
prev_dist = [0.0] * WINDOW_LEN

SAMPLE_LEN = 5000
AUDIO_SAMPLE = [int((math.sin(freq * 2 * math.pi * t/SAMPLE_LEN) + 1)/2 * 65535) for t in range(int(SAMPLE_LEN))]

# while True:
    
#     trig_pin.high()
#     utime.sleep_us(20)
#     trig_pin.low()

#     on = 0
#     off = 0

#     while echo_pin.value() == 0:
#         off = utime.ticks_us()

#     while echo_pin.value() == 1:
#         on = utime.ticks_us()

#     elapsed = on - off
#     dist = (elapsed * 0.343)/2

#     prev_dist.insert(0, dist)
#     prev_dist = prev_dist[0:WINDOW_LEN]

#     audio_pin.freq(int(sum(prev_dist)/WINDOW_LEN * 3))

#     utime.sleep_ms(20)

# while True:
#     audio_pin.freq(int((pot_pin.read_u16()/65535) * 2000 + 20))
#     freq += 20
#     utime.sleep_ms(20)

while True:

    freq = 440
    val = AUDIO_SAMPLE[utime.ticks_ms() % SAMPLE_LEN]
    #val = int(65535 * (math.sin(freq * 2 * math.pi * utime.ticks_us() / 1.0e6) + 1)/2)
    audio_pin.duty_u16(val)
    #utime.sleep_ms(1)