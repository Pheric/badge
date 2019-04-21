import rainbowPiano
from notes import *
import machine

# machine.freq(80000000)

machine.freq(40000000)
rainbowPiano.initial()

# sudo ampy -p /dev/ttyUSB0 -b 115200 put rainbowPiano.py
# sudo screen /dev/ttyUSB0 115200
# CTRL C
# CTRL a + :quit
