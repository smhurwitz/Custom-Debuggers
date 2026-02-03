import sys
sys.path.append("/Users/sienahurwitz/Documents/Hobbies/Coding/Custom Debuggers/")
from debugger import *
from hidden.hey import abc
import numpy as np
import flamegraph

import time

@homebrew_debugger()
# @flamegraph_debugger()
def heavy_lifting():
    x = 10
    time.sleep(4.9) # Simulate a slow operation
    g()
    y = 20
    h()
    abc()
    z = x + y
    np.abs([-1, 1, 3])
    b=1
    
    # desc.set_device('cpu')
    return z

def g():
    time.sleep(1.2)
    x = np.array([1, 2, 3])
    return 0

def h():
    time.sleep(0.3)
    return l()

def l():
    return "haha"

# flamegraph.start_profile_thread(fd=open("./perf.log", "w"))
heavy_lifting()
