from machine import Pin
import utime

led_pin = Pin(25, Pin.OUT)
led_pin.high()

trig_pin = Pin(15, Pin.OUT)
echo_pin = Pin(16, Pin.PULL_DOWN)

while True:
    
    trig_pin.high()
    utime.sleep_us(20)
    trig_pin.low()

    on = 0
    off = 0

    while echo_pin.value() == 0:
        off = utime.ticks_us()

    while echo_pin.value() == 1:
        on = utime.ticks_us()

    elapsed = on - off
    dist = (elapsed * 0.343)/2

    print(f"Distance: {dist:.1f}mm")

    utime.sleep(1)