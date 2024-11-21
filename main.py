import pygame
import random
import numpy
from mc_tetris.timer import Timer
from copy import copy, deepcopy

pygame.init()
screen = pygame.display.set_mode((400, 800))
clock = pygame.time.Clock()

m = [[0 for i in range(10)] for j in range(30)]
blocks = [[[0,1,0,0],
          [0,1,0,0],
          [0,1,0,0],
          [0,1,0,0]],

          [[0,1,0],
          [1,1,1],
          [0,0,0]],

          [[1,0,0],
          [1,0,0],
          [1,1,0]],

          [[1,1],
          [1,1]],

          [[1,1,0],
          [0,1,1],
          [0,0,0]],

          [[0,1,1],
          [1,1,0],
          [0,0,0]],

          [[0,1,0],
          [0,1,0],
          [1,1,0]],]

class Grid():
    def __init__(self):
        pass

    def clear(self, arr):
        for i in range(len(arr)): arr[i] = 0
    
    def update(self):
        for i in range(10, len(m)):
            f = True
            for j in range(10):
                if not m[i][j]: 
                    f = False
                    break
            if f:
                self.clear(m[i])
                for j in range(i - 1, 9, -1):
                    m[j + 1] = deepcopy(m[j])
                    self.clear(m[j])

    def draw(self):
        for i in range(10, len(m)):
            for j in range(10):
                if m[i][j]: 
                    pygame.draw.rect(screen, "red", (j * 40, (i - 10) * 40, 40, 40))

class Rules():
    def __init__(self):
        self.t = Timer(200)

    def is_over(self):
        for i in range(0, 10):
            for j in range(0,10):
                if(m[i][j]): return True
        return False
    
    def collision_v(self, a, x, y, f = True, d = 1):
        for i in range(len(a)):
            for j in range(len(a[i])):
                if not a[i][j]: continue;
                if y[i][j] + 1 >= len(m) or m[y[i][j] + 1][x[i][j]]:
                    if f: self.t.activate()
                    return True
        self.t.deactivate()
        return False

    def collision_h(self, a, x, y, d):
        for i in range(len(a)):
            for j in range(len(a[i])):
                if not a[i][j]: continue
                if x[i][j] + d < 0 or x[i][j] + d >= len(m[0]): return True
                if m[y[i][j]][x[i][j] + d]: return True
        return False
    
    def adjust(self, a, x, y):
    
    def collision(self, a, x, y):
        for i in range(len(a)):
            for j in range(len(a[i])):
                if not a[i][j]: continue
                if x[i][j] < 0 or x[i][j] >= len(m[0]):
                    self.adjust(a, x, y)
                if y[i][j] < 0 or y[i][j] >= len(m): return True
                if m[y[i][j]][x[i][j]]: return True
        return False
    
    def fixed(self, a, x, y):
        if not self.t.check(): return False
        self.t.deactivate()
        for i in range(len(a)):
            for j in range(len(a[i])):
                if a[i][j]:
                    m[y[i][j]][x[i][j]] = 1
        return True


class Shape():
    def __init__(self, pos_x, pos_y):
        self.rule = Rules()
        #self.a = deepcopy(random.choice(blocks))
        self.a = blocks[2]
        self.t_h = Timer(110)
        self.t_v = Timer(600, True)
        self.x = deepcopy(self.a)
        self.y = deepcopy(self.a)

        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                self.x[i][j] = pos_x + j
                self.y[i][j] = pos_y + i - len(self.a) + 1

    def update(self):
        if self.t_v.check():
            self.t_v.deactivate()
            self.move_v()
            self.t_v.activate()
        if self.t_h.check():
            self.t_h.deactivate()
        
        if self.rule.collision_v(self.a, self.x, self.y, False): 
            return self.rule.fixed(self.a, self.x, self.y) 

    def iput(self):
        d = pygame.key.get_pressed()
        if not self.t_h.active:
            self.move_h(d[pygame.K_RIGHT] - d[pygame.K_LEFT])
            if(d[pygame.K_e] - d[pygame.K_q]):
                self.rotate(d[pygame.K_e] - d[pygame.K_q])
            self.t_h.activate()

    def move_h(self, d):
        if self.rule.collision_h(self.a, self.x, self.y, d): return
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                self.x[i][j] += d

    def rotate(self, d):
        tmp = deepcopy(self.a)
        for i in range(len(self.a)):
            for j in range(i):
                self.a[i][j] += self.a[j][i]
                self.a[j][i] = self.a[i][j] - self.a[j][i];
                self.a[i][j] -= self.a[j][i]
        if d == -1: 
            self.a = self.a[::-1]
        elif d == 1:
            self.a = [row[::-1] for row in self.a]
        if r.collision(self.a, self.x, self.y):
            self.a = deepcopy(tmp)
        
    def move_v(self):
        if self.rule.collision_v(self.a, self.x, self.y, 1): return
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                self.y[i][j] += 1

    def draw(self):
        for i in range(len(self.a)):
            for j in range(len(self.a[i])):
                if(self.a[i][j] == 1):
                    pygame.draw.rect(screen, "red", (self.x[i][j] * 40, (self.y[i][j] - 10) * 40, 40,40))

s = Shape(4,10)
g = Grid()
r = Rules()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
    screen.fill("gray")

    key = pygame.key.get_pressed()
    g.draw()
    s.draw()
    if s.update():
        del s
        s = Shape(4,10)
    s.iput()
    g.update()

    if r.is_over():
        exit()

    pygame.display.update()
    clock.tick()