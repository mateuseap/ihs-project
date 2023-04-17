PATH = '/dev/mydev'

RD_SWITCHES = 24929
RD_PBUTTONS = 24930
WR_L_DISPLAY = 24931
WR_R_DISPLAY = 24932
WR_RED_LEDS = 24933
WR_GREEN_LEDS = 24934

seven_segment_options = {
    0 : 0b01000000,
    1 : 0b01111001, 
    2 : 0b00100100,
    3 : 0b00110000,
    4 : 0b00011001,
    5 : 0b00010010,
    6 : 0b00000010,
    7 : 0b01111000,
    8 : 0b00000000,
    9 : 0b00010000,
    "OFF" : 0b11111111
}

def seven_segment_encoder(num):
    display = 0
    num_digits = 0

    while True:
        digit = num % 10
        display |= (seven_segment_options[digit] << 8 * num_digits)
        num_digits += 1
        num = num // 10
        
        if num == 0:
            break

    for i in range (num_digits, num_digits + (4 - num_digits)):
        display |= (seven_segment_options["OFF"] << 8 * i)

    return display