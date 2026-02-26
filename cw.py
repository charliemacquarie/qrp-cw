import time

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

dot = 0.5
dash = (dot * 3)
pause = dot
letter = (dot * 3)
space = (dot * 7)


LINE = 91

with request_lines(
    "/dev/gpiochip1",
    consumer="blink-example",
    config={
        LINE: LineSettings(
            direction=Direction.OUTPUT, output_value=Value.ACTIVE
        )
    },
) as request:
    while True:
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(dot)
        request.set_value(LINE, Value.INACTIVE)
        time.sleep(pause)
        request.set_value(LINE, Value.ACTIVE)
        time.sleep(dash)
        request.set_value(LINE, Value.INACTIVE)

