#!/usr/bin/env python3

import sys
from os import system

ARGCOPY = sys.argv
STRARG = "./st.py "
NoOfTimes = 1
if len(ARGCOPY) > 1:
    for arg in ARGCOPY[1:]:
        if int(arg) == 0:
            STRARG += " " + arg
            ARGCOPY.remove(arg)
        else:
            NoOfTimes = int(arg)
for i in range(NoOfTimes):
    system(STRARG)
