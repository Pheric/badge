import math

import machine
import time
import neopixel
from notes import *
import random

import esp32

pin13 = machine.Pin(13)
pin16 = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
speaker = machine.PWM(pin13)
speaker.duty(0)

current = 0
thresh = 500
colors = [(0,0,0),(0,0,0)]

t0 = machine.TouchPad(machine.Pin(4))
t1 = machine.TouchPad(machine.Pin(15))
t2 = machine.TouchPad(machine.Pin(12))
t3 = machine.TouchPad(machine.Pin(14))

t0.config(thresh)
t1.config(thresh)
t2.config(thresh)
t3.config(thresh)

pins = [t0, t1, t2, t3]

np = neopixel.NeoPixel(machine.Pin(25), 10)
# np = neopixel.NeoPixel(machine.Pin(25), 10, bpp=4)

hx = machine.Pin(27, machine.Pin.PULL_UP)

esp32.wake_on_touch(True)


theme = []
muted = False
def initial():
    onReset()

    for i in range(10):
        np[i] = (0, 0, 0)

    print("Theme menu\n(-?) (+r) (+g) (+b)")
    global theme
    theme = pickTheme()
    print("Chosen: %s" % theme)
    onSuccess()
    for i in range(10):
        np[i] = theme
    np.write()

    while True:
        if touched(2, 3):
            zelda()

            for i in range(10):
                np[i] = theme
            np.write()
        elif touched(0, 3):
            global muted
            muted = not muted
            play_note(F5, .2, False)
            onSuccess()

            for i in range(10):
                np[i] = theme
            np.write()


def pickTheme():
    rgb = [10, 100, 50]
    lim = False
    while True:
        if touched(0, 1, 2, 3):
            break
        elif touched(0, 1):
            if rgb[0] > 0:
                rgb[0] -= 1
                lim = False
            else:
                lim = True
        elif touched(1):
            if rgb[0] < 255:
                rgb[0] += 1
                lim = False
            else:
                lim = True
        elif touched(0, 2):
            if rgb[1] > 0:
                rgb[1] -= 1
                lim = False
            else:
                lim = True
        elif touched(2):
            if rgb[1] < 255:
                rgb[1] += 1
                lim = False
            else:
                lim = True
        elif touched(0, 3):
            if rgb[2] > 0:
                rgb[2] -= 1
                lim = False
            else:
                lim = True
        elif touched(3):
            if rgb[2] < 255:
                rgb[2] += 1
                lim = False
            else:
                lim = True

        np[9] = rgb
        if lim:
            np[0] = (255, 0, 0)
        else:
            np[0] = (0, 0, 0)
        np.write()
        time.sleep(.0075)

    return rgb


def onSuccess():
    for i in range(10):
        np[i] = (0, 255, 0)
    np.write()
    time.sleep(1)


def touched(*buttons):
    ok = 1
    for i, e in enumerate(buttons):
        if not pins[e].read() < thresh:
            ok = False

    return ok


def insert(led, lim=9):
    for i in range(lim):
        np[i] = np[i + 1]
    np[lim] = led

    np.write()


def onReset():
    for i in range(10):
        np[i] = (255, 0, 0)
    np.write()
    time.sleep(1)
    for i in range(10):
        np[i] = (0, 0, 0)
    np.write()


def play_note(freq: int, play_time: float = .2, display=True):
    """
    Plays a note of frequency `freq` for duration `play_time`, and lights up a random LED for fun
    :param freq: The frequency of the note to play, in hz
    :param play_time: The duration of the note, in seconds
    :param display: Whether to show random colors when the sound is played
    :return: Null
    """
    global muted
    if display:
        insert((random.randrange(0, 150), random.randrange(0, 150), random.randrange(0, 150)))
        time.sleep(play_time)
    if muted:
        return
    speaker.duty(100)
    speaker.freq(freq)
    time.sleep(play_time)
    speaker.duty(0)


# This function checks the charging stats
def battery():
    if hx.value() == 0:
        print("Charged")
    else:
        print("Charging")


def zelda():
    """
        Play the main theme from Link's awakening.
        :return:
        """
    print("Playing Zelda..")

    play_note(AS5, .314)
    time.sleep(.091)
    play_note(F5, .522)
    play_note(AS5)
    play_note(AS5)
    play_note(C6)
    play_note(D6)
    play_note(DS6)
    # 1.19
    play_note(F6, .506)
    time.sleep(.507)
    play_note(F6)
    time.sleep(.1)
    play_note(F6)
    time.sleep(.1)
    play_note(FS6)
    play_note(GS6)
    # 3.07
    play_note(AS6, .517)
    # Top of the first swell

    play_note(AS6)
    time.sleep(.1)
    play_note(AS6)
    time.sleep(.1)
    play_note(GS6)
    play_note(FS6)
    # 4.26
    play_note(GS6, .304)
    play_note(FS6)
    play_note(F6, .507)
    time.sleep(.241)
    play_note(F6, .304)
    time.sleep(.1)
    # 6.15
    play_note(DS6, .315)
    play_note(F6)
    play_note(FS6, .517)
    time.sleep(.304)
    play_note(F6)
    time.sleep(.1)
    play_note(DS6)
    time.sleep(.1)
    # 8.03
    play_note(CS6)
    play_note(DS6)
    play_note(F6, .506)
    time.sleep(.304)
    play_note(DS6)
    time.sleep(.1)
    play_note(CS6)
    time.sleep(.1)
    # 9.22
    play_note(C6, .304)
    play_note(D6)
    play_note(E6, .497)
    time.sleep(.304)
    play_note(G6, .314)
    time.sleep(.1)
    # 11.11
    play_note(F6)
    time.sleep(.1)
    play_note(math.ceil((AS5 + F5) / 2))
    time.sleep(.001)
    play_note(math.ceil((AS5 + F5) / 2))
    time.sleep(.001)
    play_note(math.ceil((AS5 + F5) / 2))
    time.sleep(.1)
    play_note(math.ceil((AS5 + F5) / 2))
    time.sleep(.001)
    play_note(math.ceil((AS5 + F5) / 2))
    time.sleep(.001)
    play_note(math.ceil((AS5 + F5) / 2))

    print("Done")
