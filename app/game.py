import os
from fcntl import ioctl
from utils import *

def red_leds_on(fd):
    data = 0b111111111111111111
    ioctl(fd, WR_RED_LEDS)
    os.write(fd, data.to_bytes(4, 'little'))
    print(f'>>> red leds on!')

def green_leds_on(fd):
    data = 0b111111111
    ioctl(fd, WR_GREEN_LEDS)
    os.write(fd, data.to_bytes(4, 'little'))
    print(f'>>> green leds on!')

def read_button(fd):
    ioctl(fd, RD_PBUTTONS)
    button = os.read(fd, 1)
    button = bin(int.from_bytes(button , 'little'))
    print(f'>>> button {button}')
    return button

def show_seven_segment(fd, num, display):
    data = seven_segment_encoder(num)
    ioctl(fd, display)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print(f'>>> wrote {retval} bytes')

def main():
    fd = os.open(PATH, os.O_RDWR)

    # print('Input a single number that will appear on 7-segment display: ')
    # number = int(input())

    # show_seven_segment(fd, number, WR_L_DISPLAY)
    # show_seven_segment(fd, number, WR_R_DISPLAY)

    green_leds_on(fd)

if __name__ == '__main__':
    main()