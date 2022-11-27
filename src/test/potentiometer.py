from machine import Pin, ADC
import utime

led_pin = Pin(25, Pin.OUT)
led_pin.high()

pot_pin = ADC(Pin(26))

while True:

    print(pot_pin.read_u16())

    utime.sleep(0.1)