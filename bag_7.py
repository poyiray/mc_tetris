import random
from copy import deepcopy
from shape import name, typ, weight
from basic import top
from tetro import Tetro

class Bag_7():
    def __init__(self):
        self.queue = []
        self.queue_t = []
        random.shuffle(name)
        for i in range(7):
            self.queue.append(Tetro((name[i], random.choices(typ, weight)[0]), 4, top - 2))

        self.queue_name = deepcopy(name)
        random.shuffle(name)
        self.queue_t = deepcopy(name)

        self.hh = 0
        self.tt = len(self.queue_name) % 7

    def get(self):
        x = self.queue[self.hh]
        self.hh = (self.hh + 1) % 7

        self.queue[self.tt] = Tetro((self.queue_t.pop(), random.choices(typ, weight)[0]), 4, top - 2)
        self.tt = (self.tt + 1) % 7

        if not len(self.queue_t):
            random.shuffle(name)
            self.queue_t = deepcopy(name)
        return x