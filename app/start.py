from utils import *

fd = os.open(PATH, os.O_RDWR)
print('Arquivo aberto com sucesso!')

def reset():
    global fd

    seven_segment(fd=fd, num=0, display=WR_L_DISPLAY, show_output_msg=True)
    seven_segment(fd=fd, num=0, display=WR_R_DISPLAY, show_output_msg=True)
    red_leds(fd=fd, on=False, sequence=False, show_output_msg=True)
    green_leds(fd=fd, on=False, sequence=False, show_output_msg=True)
    read_switches(fd=fd, show_output_msg=True)
    read_button(fd=fd, show_output_msg=True)

    os.close(fd)
    print('Arquivo fechado com sucesso!')

def start():
    global fd

    print('\nAperte o botão de START para o show começar :)\n')

    while True:
        button = read_button(fd=fd, show_output_msg=False)
        if BUTTONS_OPTIONS[button] == "START":
            break
    
    # Showing numbers on seven segment displays
    seven_segment(fd=fd, num=1, display=WR_L_DISPLAY, show_output_msg=True)
    seven_segment(fd=fd, num=3, display=WR_R_DISPLAY, show_output_msg=True)

    # Turning on all leds
    red_leds(fd=fd, on=True, sequence=False, show_output_msg=True)
    green_leds(fd=fd, on=True, sequence=False, show_output_msg=True)
    
    # Turning off all leds
    red_leds(fd=fd, on=False, sequence=False, show_output_msg=True)
    green_leds(fd=fd, on=False, sequence=False, show_output_msg=True)

    # Turning on one led at a time in sequence
    red_leds(fd=fd, sequence=True, show_output_msg=True)
    green_leds(fd=fd, sequence=True, show_output_msg=True)

    print('\nDesligue todos os switches para o jogo começar!\n')

    while True:
        switches = read_switches(fd=fd, show_output_msg=False)
        if switches == '0b111111111111111111':
            break

    reset()

start()