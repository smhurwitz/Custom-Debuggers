import time
from debugger import homebrew_debugger
import sys
import numpy as np

@homebrew_debugger(threshold)
def complicated():
    a = 1
    nestc()
    b = 2
    c = a + b
    nesta()
    d = np.array(range(100000000))
    e = d ** 3.3
    time.sleep(0.75)
    nestb()
    d = c * 1.0 / b
    return c

def nesta():
    time.sleep(0.3)

def nestb():
    time.sleep(1)
    nesta()

def nestc():
    nestb()
    time.sleep(1.33)

complicated()