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

blocks = [pygame.image.load("./Textures/Stone.webp"),
          pygame.image.load("./Textures/Block_of_Diamond.webp"),
          pygame.image.load("./Textures/Block_of_Iron.webp"),
          pygame.image.load("./Textures/Diamond_Ore.webp"),
          pygame.image.load("./Textures/Iron_Ore.webp"),
          pygame.image.load("./Textures/Oak_Planks.webp"),
          pygame.image.load("./Textures/Coal_Ore.webp"),
          pygame.image.load("./Textures/Bookshelf.webp"),
          pygame.image.load("./Textures/Cobblestone.webp"),
          pygame.image.load("./Textures/Crafting_Table.webp"),
          pygame.image.load("./Textures/Glowstone.webp"),
          pygame.image.load("./Textures/Grass_Block.webp"),
          pygame.image.load("./Textures/Off_Furnace.webp"),
          pygame.image.load("./Textures/On_Furnace.webp"),
          pygame.image.load("./Textures/Hay_Bale.webp"),
          pygame.image.load("./Textures/Pumpking_Light.webp"),
          pygame.image.load("./Textures/Carved_Pumpkin.webp"),]

sounds = [pygame.mixer.Sound("./sound/Grass_dig3.mp3"),
               pygame.mixer.Sound("./sound/Metal_dig3.mp3"),
               pygame.mixer.Sound("./sound/Wood_dig3.mp3")]

block_sound_idx = [1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 0, 1, 1, 0, 1, 1]

trunk = [pygame.image.load("./Textures/Birch.webp"),
         pygame.image.load("./Textures/Oak.webp")]

trunk_sound_idx = [2, 2]

class Tnt():
    def __init__(self):
        self.frame = 0

    def __bool__(self):
        return True
    
    def draw(self, x, y, alpha = 255):
        image = pygame.image.load("./Textures/TNT.webp")
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
    
    def sound(self):
        pygame.mixer.Sound("./sound/Grass_dig3.mp3").play()


class Block():
    def __init__(self):
        self.typ = random.randrange(len(blocks))
        self.frame = 0

    def __bool__(self):
        return True
    
    def draw(self, x, y, alpha = 255):
        image = blocks[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
    
    def sound(self):
        sounds[block_sound_idx[self.typ]].play()

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

    def sound(self):
        sounds[trunk_sound_idx[self.typ]].play()

typ = [Tnt, Block, Tree]
weight = [0.1, 0.7, 0.2]
