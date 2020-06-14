import os
import numpy as np
import random
import datetime
from z3 import *
import signal
import time


dirName = sys.argv[1]
targetName = sys.argv[2]

fileList = os.listdir(dirName)
for name in fileList:
    if name.endswith(".c"):
        os.system("python3 ./CLIMain.py parsectoboogie " + dirName + name + " " + targetName + name+".bpl")

