import time

import machine
import neopixel
from machine import I2C, Pin

import tm1637
from bmp180 import BMP180

num_leds = 12
full_brightness = 255
half_brightness = 127
quarter_brightness = 64
next_brightness = 32

tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
bus = I2C(scl=Pin(4), sda=Pin(5), freq=100000)

bmp180 = BMP180(bus)
np = neopixel.NeoPixel(machine.Pin(14), num_leds)


def get_temperature_and_write_to_display():
    temp = bmp180.temperature
    tm.temperature(int(temp))
    return temp


def blink_led(led_num, red=0, green=0, blue=0, flash_red=0, flash_green=0, flash_blue=0):
    count = 0
    while count < 3:
        turn_led_on(led_num, red=red, green=green, blue=blue)
        time.sleep(0.01)
        turn_led_on(led_num, red=flash_red, green=flash_green, blue=flash_blue)
        time.sleep(0.01)
        count += 1


def turn_led_on(led_num, red=0, green=0, blue=0):
    np[led_num] = (red, green, blue)
    np.write()


def turn_led_off(led_num):
    np[led_num] = (0, 0, 0)
    np.write()


def clear():
    switch_all_leds()


def switch_all_leds(red=0, green=0, blue=0):
    np.fill((red, green, blue))
    np.write()


def do_leds(led_num, red=0, green=0, blue=0, flash_red=0, flash_green=0, flash_blue=0):
    switch_all_leds(red=flash_red, green=flash_green, blue=flash_blue)
    if led_num > 0:
        turn_led_on(led_num - 1, red=red, green=green, blue=blue)
    blink_led(led_num, red=red, green=green, blue=blue,
              flash_red=flash_red, flash_green=flash_green, flash_blue=flash_blue)
    led_num += 1
    return led_num


def initialise():
    tm.show('Init')
    led = 0
    loop = 0
    while loop != 200:
        if led <= num_leds - 1:
            led = do_leds(led, green=quarter_brightness, flash_green=next_brightness)
        else:
            led = 0
        loop += 1


led = 0
last_temperature = get_temperature_and_write_to_display()

initialise()

while True:
    current_temperature = get_temperature_and_write_to_display()
    print("last_temperature : {} : current_temperature {}".format(int(last_temperature), int(current_temperature)))
    loop = 0
    printed = False
    while loop != 200:
        if led <= num_leds - 1:
            if int(last_temperature) < int(current_temperature):
                if not printed:
                    print("Temperature is increasing was {}, now {}".format(last_temperature, current_temperature))
                    printed = True

                led = do_leds(led, red=quarter_brightness, flash_red=next_brightness)

            elif int(last_temperature) > int(current_temperature):
                if not printed:
                    print("Temperature is decreasing was {}, now {}".format(last_temperature, current_temperature))
                    printed = True

                led = do_leds(led, blue=quarter_brightness, flash_blue=next_brightness)

            else:
                clear()
        else:
            led = 0
        loop += 1
    last_temperature = current_temperature
