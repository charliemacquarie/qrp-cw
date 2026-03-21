import time

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from continuous import make_morse, blink_morse, blink_idle

# MORSE TIMINGS
dot = 0.5
dash = (dot * 3)
pause = dash
space = (dot * 7)

TEST_STRING = 'KN6HLC sending 73s!'

morse = make_morse(TEST_STRING)

LINE = 92
cycle = 10

blink_morse(LINE, morse)

blink_idle(LINE, cycle)
