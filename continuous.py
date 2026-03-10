import time

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                    'C':'-.-.', 'D':'-..', 'E':'.',
                    'F':'..-.', 'G':'--.', 'H':'....',
                    'I':'..', 'J':'.---', 'K':'-.-',
                    'L':'.-..', 'M':'--', 'N':'-.',
                    'O':'---', 'P':'.--.', 'Q':'--.-',
                    'R':'.-.', 'S':'...', 'T':'-',
                    'U':'..-', 'V':'...-', 'W':'.--',
                    'X':'-..-', 'Y':'-.--', 'Z':'--..',
                    '1':'.----', '2':'..---', '3':'...--',
                    '4':'....-', '5':'.....', '6':'-....',
                    '7':'--...', '8':'---..', '9':'----.',
                    '0':'-----', ', ':'--..--', '.':'.-.-.-',
                    '?':'..--..', '/':'-..-.', '-':'-....-',
                    '(':'-.--.', ')':'-.--.-', ' ': ' '}

CHARACTERS_AVAILABLE = [key for key in MORSE_CODE_DICT.keys()]

def make_morse(string: str):
    """
    Convert a text string to morse code, returning a string of dots ('.') and
    dashes ('-') to represent the characters in morse. String is made
    upper-case, any non-space white space is stripped, and any
    non-available character is removed.

    See available characters in continuous.CHARACTERS_AVAILABLE.

    :param string str: the string to be converted to morse
    """

    morse_string = ''

    for c in string.upper().strip():
        if c not in CHARACTERS_AVAILABLE:
            m = ''
        else:
            m = MORSE_CODE_DICT[c]

        morse_string += m
        morse_string += ' '

    return morse_string

def blink_morse(chip_line: int, morse_string: str):
    """
    Use a specified gpio pin to send signals which will blink an LED
    (if one is connected to the pin) according to a specified morse code
    string represented in dots (as '.') and dashes (as '-')

    :param chip_line int: the line number on the gpiochip which should send signal
    :param morse_string str: the string of '.' and '-' representing the text to
    be sent
    """
    # ADD IN FILTERINGS TO ENSURE MORSE

    # MORSE TIMINGS
    # MAKE THESE EDITABLE?
    dot = 0.5
    dash = (dot * 3)
    pause = dash
    space = (dot * 7)

    # ENABLE SPECIFY THE gpiochip?
    with request_lines(
        "/dev/gpiochip1",
        consumer="blink-morse",
        config={
            chip_line: LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
                )
            },
        ) as request:
            for i in morse_string:
                if i == '.':
                    request.set_value(chip_line, Value.ACTIVE)
                    time.sleep(dot)
                if i == '-':
                    request.set_value(chip_line, Value.ACTIVE)
                    time.sleep(dash)
                if i == ' ':
                    request.set_value(chip_line, Value.INACTIVE)
                    time.sleep(pause)

                request.set_value(chip_line, Value.INACTIVE)
                time.sleep(dot)

def blink_idle(chip_line: int):
    """
    Use a specified gpio pin to send signals which will blink an LED
    (if one is connected to the pin) on and off at an on:off ratio of 1:3

    :param chip_line int: the line number on the gpiochip which should send signal
    """

    # TIMINGS
    # MAKE THESE EDITABLE?
    dot = 0.5
    dash = (dot * 3)

    # ENABLE SPECIFY THE gpiochip?
    with request_lines(
        "/dev/gpiochip1",
        consumer="blink-idle",
        config={
            chip_line: LineSettings(
                direction=Direction.OUTPUT, output_value=Value.ACTIVE
                )
            },
        ) as request:
            while True:
                request.set_value(chip_line, Value.ACTIVE)
                time.sleep(dot)
                request.set_value(chip_line, Value.INACTIVE)
                time.sleep(dash)
