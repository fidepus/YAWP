#!/usr/bin/env python
 # -*- coding: utf-8 -*-
# Write some message on the display.
# This project uses https://github.com/dbrgn/RPLCD.

from __future__ import print_function, division, absolute_import, unicode_literals

import sys

from RPLCD import CharLCD
from RPLCD import Alignment, CursorMode, ShiftMode
from RPLCD import cursor, cleared

try:
        input = raw_input
except NameError:
        pass

try:
        unichr = unichr
except NameError:
        unichr = chr


lcd = CharLCD()

# Initialize display. All values have default values and are therefore
# optional.
#lcd = CharLCD(pin_rs=15, pin_rw=18, pin_e=16, pins_data=[21, 22, 23, 24],
#                      numbering_mode=GPIO.BOARD,
#                                    cols=20, rows=4, dotsize=8)

lcd.clear()
lcd.write_string('********************')
lcd.cursor_pos = (1, 0)
lcd.write_string('*   Hello          *')
lcd.cursor_pos = (2, 0)
lcd.write_string('*         world!   *')
lcd.cursor_pos = (3, 0)
lcd.write_string('********************')
