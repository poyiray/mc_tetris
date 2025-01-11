import pygame
import random
from basic import m, screen
name = ['I', 'T', 'J', 'O', 'Z', 'S', 'L']

pos = {'I':[[(-1, 0), (0, 0), (1, 0), (2, 0)],
              [(1, -1), (1, 0), (1, 1), (1, 2)],
              [(2, 1), (1, 1), (0, 1), (-1, 1)],
              [(0, 2), (0, 1), (0, 0), (0, -1)]],

          "J":[[(-1, -1), (-1, 0), (0, 0), (1, 0)],
               [(1, -1), (0, -1), (0, 0), (0, 1)],
               [(1, 1), (1, 0), (0, 0), (-1, 0)],
               [(-1, 1), (0, 1), (0, 0), (0, -1)]],

          "L":[[(-1, 0), (0, 0), (1, 0), (1, -1)],
               [(0, -1), (0, 0), (0, 1), (1, 1)],
               [(1, 0), (0, 0), (-1, 0), (-1, 1)],
               [(0, 1), (0, 0), (0, -1), (-1, -1)]],

          "O":[[(0, 0), (1, 0), (0, -1), (1, -1)],
               [(0, 0), (1, 0), (0, -1), (1, -1)],
               [(0, 0), (1, 0), (0, -1), (1, -1)],
               [(0, 0), (1, 0), (0, -1), (1, -1)]],

          "S":[[(-1, 0), (0, 0), (0, -1), (1, -1)],
               [(0, -1), (0, 0), (1, 0), (1, 1)],
               [(1, 0), (0, 0), (0, 1), (-1, 1)],
               [(0, 1), (0, 0), (-1, 0), (-1, -1)]],

          "Z":[[(-1, -1), (0, -1), (0, 0), (1, 0)],
               [(1, -1), (1, 0), (0, 0), (0, 1)],
               [(1, 1), (0, 1), (0, 0), (-1, 0)],
               [(-1, 1), (-1, 0), (0, 0), (0, -1)]],
          
          "T":[[(-1, 0), (0, 0), (0, -1), (1, 0)],
               [(0, -1), (0, 0), (1, 0), (0, 1)],
               [(1, 0), (0, 0), (0, 1), (-1, 0)],
               [(0, 1), (0, 0), (-1, 0), (0, -1)]]}

blocks = {"TNT": pygame.image.load("./Textures/TNT.webp"),
          "Stone": pygame.image.load("./Textures/Stone.webp")}

trunk = [pygame.image.load("./Textures/Birch.webp"),
         pygame.image.load("./Textures/Oak.webp")]

class Tnt():
    def __init__(self):
        self.frame = 0

    def __bool__(self):
        return True
    
    def draw(self, x, y, alpha = 255):
        image = blocks["TNT"]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))

class Stone():
    def __init__(self):
        self.frame = 0

    def __bool__(self):
        return True
    
    def draw(self, x, y, alpha = 255):
        image = blocks["Stone"]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))

class Tree():
    def __init__(self):
        self.typ = random.randrange(len(trunk))
        self.frame = 0

    def __bool__(self):
        return True
    
    def draw(self, x, y, alpha = 255):
        image = trunk[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))

typ = [Tnt, Stone, Tree]
