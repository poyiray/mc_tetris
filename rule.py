from copy import deepcopy
from basic import bottom, m, width
from timer import Timer
import pygame

class Rules():
    def __init__(self):
        self.t = Timer(800)

    def is_over(self):
        #上方如果堆积了方块就是越界了
        for i in range(0, 10):
            for j in range(0,10):
                if m[i][j]: return True
        return False
    
    def collision_v(self, x, y):
        for i in range(len(y)):
            if y[i] + 1 >= bottom or m[y[i] + 1][x[i]]:
                self.t.activate()
                return True
        self.t.deactivate()
        return False

    def collision_h(self, x, y, d):
        for i in range(len(x)):
            if x[i] + d < 0 or x[i] + d >= width or m[y[i]][x[i] + d]:
                return True
        return False
    
    def fixed(self, box, x, y):
        if not self.t.check(): return False
        self.t.deactivate()
        for i in range(len(x)):
            m[y[i]][x[i]] = deepcopy(box[i])
        return True
