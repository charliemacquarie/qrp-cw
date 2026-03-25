import time
import math
from pathlib import Path
from os import listdir, remove
from os.path import isfile, join
from multiprocessing import Process

from gpiod import request_lines, LineSettings
from gpiod.line import Direction, Value

from continuous import make_morse, blink_morse, blink_idle

# MORSE TIMINGS
dot = 0.5
dash = (dot * 3)
pause = dash
space = (dot * 7)

#TEST_STRING = 'KN6HLC sending 73s!'

#morse = make_morse(TEST_STRING)

# gpio lines right now should be:
# 91, 92, 94

LINE = 92
cycle = 30

LINES = [91, 92, 93]

# NOW come back in and make a loop that actually looks in the dirs and
# goes to idle if nothing.
#blink_morse(LINE, morse)

#blink_idle(LINE, cycle)

base_dir = str(Path.home())

stream_0 = base_dir + '/transmit-data/stream-0'
stream_1 = base_dir + '/transmit-data/stream-1'
stream_2 = base_dir + '/transmit-data/stream-2'

STREAMS = [stream_0, stream_1, stream_2]

# THIS DOES NEED to have a thing that gets it back on the second
def run_cw(directory: str, chip_line: int, cycle_time: int):
    """
    Run the CW transmit using input from a supplied directory (as .txt files)

    :param directory str: the directory containing the .txt files to be transmitted
    :param chip_line int: the line number on the gpiochip which should send signal
    :param cycle_time int: number of secs to blink the idle pattern
    """

    while True:
        files = [join(directory, f) for f in listdir(directory) if isfile(join(directory, f))]
        if files:
            for f in files:
                with open(f, 'r') as file:
                    morse = make_morse(file.read())

                blink_morse(chip_line, morse)

                remove(f)

                time.sleep(math.ceil(time.time()) - time.time())

        blink_idle(chip_line, cycle_time)

if __name__  == '__main__':
    Process(target=run_cw, args=(STREAMS[0], LINES[0], 30)).start()
    Process(target=run_cw, args=(STREAMS[1], LINES[1], 30)).start()
    Process(target=run_cw, args=(STREAMS[2], LINES[2], 30)).start()
