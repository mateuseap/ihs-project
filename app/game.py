import os
from fcntl import ioctl
from utils import *

def show_seven_segment(fd, num, display):
    data = seven_segment_encoder(num)
    ioctl(fd, display)
    retval = os.write(fd, data.to_bytes(4, 'little'))
    print(f'>>> wrote {retval} bytes')

def main():
    fd = os.open(PATH, os.O_RDWR)

    print('Input a single number that will appear on 7-segment display: ')
    number = int(input())

    show_seven_segment(fd, number, WR_L_DISPLAY)
    show_seven_segment(fd, number, WR_R_DISPLAY)

if __name__ == '__main__':
    main()