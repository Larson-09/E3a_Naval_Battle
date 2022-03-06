"""
@author LAUDE Jordan and SARLAT Meven
"""

from enum import Enum

class State(Enum):
    NONE = "_"
    S = "S"
    V = "V"
    R = "R"
    T = "T"
    C = "C"

class Direction(Enum) :
    NONE = 0
    TOP = 1
    RIGHT = 2
    BOTTOM = 3
    LEFT = 4
