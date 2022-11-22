import pyfirmata
import time

def blink_light(pin, interval):
    while True:
        light = board.digital[pin].read()
        if light == 1:
            board.digital[pin].write(0)
        else:
            board.digital[pin].write(1)
        time.sleep(interval)

def offset_blinking(p1, p2):
    offsetCounter = 0
    while True:
        light1 = board.digital[p1].read()
        if light1 == 1:
            board.digital[p1].write(0)
        else:
            board.digital[p1].write(1)

        light2 = board.digital[p2].read()
        if light2 == 1:
            board.digital[p2].write(0)
        elif offsetCounter == 2:
            board.digital[p2].write(1)
            offsetCounter -= 4
        offsetCounter += 1

        time.sleep(1)

def cycle_colour(pin, brightness_incr, interval):
    while True:
        brightness = 0
        while brightness <= 1:
            board.digital[pin].write(brightness)
            brightness += brightness_incr
            time.sleep(interval)
        time.sleep(interval/brightness_incr)
        board.digital[pin].write(0)
        time.sleep(2*interval/brightness_incr)

def cycle_colours(interval=0.1):
    # 11 is red, 10 is green, 9 is blue
    rgb = {11: 0, 10: 0, 9: 0}
    cur_color = 11
    while True:
        rgb[cur_color] += 0.025
        if rgb[cur_color] >= 1:
            cur_color = cur_color + 1 if cur_color < 11 else 9
            rgb[cur_color - 1 if cur_color > 9 else 11] = 0
        board.digital[11].write(rgb[11])
        board.digital[10].write(rgb[10])
        board.digital[9].write(rgb[9])
        time.sleep(interval)

def isHexColor(str):
    if len(str) != 6:
        return False
    try:
        int(str, 16)
    except ValueError:
        return False
    return True

def hex_to_float(val):
    return int(val, 16)/255

def get_rgb(color):
    if not isHexColor(color):
        return 0, 0, 0
    return hex_to_float(color[0:2]),  hex_to_float(color[2:4]), hex_to_float(color[4:6])

def write_led_rgb(red_pin, green_pin, blue_pin, red=0, green=0, blue=0):
    board.digital[red_pin].write(red)
    board.digital[green_pin].write(green)
    board.digital[blue_pin].write(blue)

def switch_light(red_pin, green_pin, blue_pin):
    print()
    while True:
        color = input("")
        if color == "s":
            write_led_rgb(red_pin, green_pin, blue_pin, 0.5, 0, 0)
        elif color == "d":
            write_led_rgb(red_pin, green_pin, blue_pin, 0, 0.5, 0)
        elif color == "f":
            write_led_rgb(red_pin, green_pin, blue_pin, 0, 0, 0.5)

def set_light_to_hex(red_pin, green_pin, blue_pin, color):
    red, green, blue = get_rgb(color)
    write_led_rgb(red_pin, green_pin, blue_pin, red, green, blue)

def set_rgb_led(red_pin, green_pin, blue_pin):
    while True:
        color = input("Enter a hex color: ")
        if not isHexColor(color):
            print("Invalid hex color")
            continue
        set_light_to_hex(red_pin, green_pin, blue_pin, color)

def fade_colour_to_colour(red_pin, green_pin, blue_pin, color1, color2, interval=3, steps=100):
    if not isHexColor(color1) or not isHexColor(color2):
        return
    r1, g1, b1 = get_rgb(color1)
    r2, g2, b2 = get_rgb(color2)
    for step in range(0, steps):
        red = r1 + (r2 - r1) * step/steps
        green = g1 + (g2 - g1) * step/steps
        blue = b1 + (b2 - b1) * step/steps
        write_led_rgb(red_pin, green_pin, blue_pin, red, green, blue)
        time.sleep(interval/steps)

def fade_colours(red_pin, green_pin, blue_pin):
    while True:
        color1 = input("Enter a hex color: ")
        if not isHexColor(color1):
            print("Invalid hex color")
            continue
        color2 = input("Enter a hex color: ")
        if not isHexColor(color2):
            print("Invalid hex color")
            continue
        set_light_to_hex(red_pin, green_pin, blue_pin, color1)
        time.sleep(1)
        fade_colour_to_colour(red_pin, green_pin, blue_pin, color1, color2)

def cycle_rgb(red_pin, green_pin, blue_pin, interval=2):
    while True:
        fade_colour_to_colour(red_pin, green_pin, blue_pin, "ff0000", "00ff00", interval)
        fade_colour_to_colour(red_pin, green_pin, blue_pin, "00ff00", "0000ff", interval)
        fade_colour_to_colour(red_pin, green_pin, blue_pin, "0000ff", "ff0000", interval)

def seven_seg_display():
    board.digital[2].write(1)
    input("set digit 2 to 1")

board = pyfirmata.Arduino('/dev/tty.usbmodem143301')

def setup():
    # 2 is fan
    # board.digital[11].mode = pyfirmata.PWM # red
    # board.digital[10].mode = pyfirmata.PWM # green
    # board.digital[9].mode = pyfirmata.PWM # blue
    return

def main():
    try:
        setup()
        seven_seg_display()
    except KeyboardInterrupt:
        for i in range(2, len(board.digital)):
            board.digital[i].write(0)
            print(f'wrote 0 to pin {i}')

if __name__ == '__main__':
    main()