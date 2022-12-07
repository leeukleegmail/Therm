from helpers import initialise, clear, get_temperature_and_write_to_display, do_leds_clockwise, do_leds_anticlockwise, \
    quarter_brightness, next_brightness

last_temperature = initialise()

while True:
    clear()
    current_temperature = get_temperature_and_write_to_display()

    if int(last_temperature) < int(current_temperature):
        print("Temperature is increasing was {}, now {}".format(last_temperature, current_temperature))
        do_leds_clockwise(red=quarter_brightness, flash_red=next_brightness)

    elif int(last_temperature) > int(current_temperature):
        print("Temperature is decreasing was {}, now {}".format(last_temperature, current_temperature))
        do_leds_anticlockwise(blue=quarter_brightness, flash_blue=next_brightness)
    else:
        print("Temperature is the same was {}, is {}".format(last_temperature, current_temperature))

    last_temperature = current_temperature
