import os, sys
from fcntl import ioctl
from utils import *

def display_seven_segment(num, display):
    data = seven_segment_encoder(num)
    ioctl(os.open(sys.argv[1], os.O_RDWR), display)
    retval = os.write(os.open(sys.argv[1], os.O_RDWR), data.to_bytes(4, 'little'))
    print(retval)

def main():
    print('Insira um digito para aparecer no display de 7 segmentos: ')
    number = input()

    display_seven_segment(number, WR_L_DISPLAY)
    display_seven_segment(number, WR_R_DISPLAY)

if __name__ == '__main__':
    main()