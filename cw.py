import time

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from continuous import make_morse

# MORSE TIMINGS
dot = 0.5
dash = (dot * 3)
pause = dash
space = (dot * 7)

TEST_STRING = 'KN6HLC sending 73s!'

morse = make_morse(TEST_STRING)

LINE = 91

# REPLACE this part with the actual function and check it works...
with request_lines(
    "/dev/gpiochip1",
    consumer="blink-example",
    config={
        LINE: LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
            )
        },
    ) as request:
        for i in morse:
            if i == '.':
                request.set_value(LINE, Value.ACTIVE)
                time.sleep(dot)
            if i == '-':
                request.set_value(LINE, Value.ACTIVE)
                time.sleep(dash)
            if i == ' ':
                request.set_value(LINE, Value.INACTIVE)
                time.sleep(pause)

            request.set_value(LINE, Value.INACTIVE)
            time.sleep(dot)
