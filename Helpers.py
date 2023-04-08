from enum import Enum


class State(Enum):
    LOADED = 1
    FLYING = 2
    ANCHORED = 3
    RECALL = 4
