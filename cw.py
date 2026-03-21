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

# gpio lines right now should be:
# 91, 92, 94

LINE = 92
cycle = 10


# NOW come back in and make a loop that actually looks in the dirs and
# goes to idle if nothing.
blink_morse(LINE, morse)

blink_idle(LINE, cycle)
