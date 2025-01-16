import pygame
import random
from timer import Timer
from basic import m, screen, top, bottom, width
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
          pygame.image.load("./Textures/Coal_Ore.webp"),
          pygame.image.load("./Textures/Cobblestone.webp"),
          pygame.image.load("./Textures/Crafting_Table.webp"),
          pygame.image.load("./Textures/Glowstone.webp"),
          pygame.image.load("./Textures/Grass_Block.webp"),
          pygame.image.load("./Textures/Off_Furnace.webp"),
          pygame.image.load("./Textures/On_Furnace.webp")]

sounds = [pygame.mixer.Sound("./sound/Grass_dig3.mp3"),
               pygame.mixer.Sound("./sound/Metal_dig3.mp3"),
               pygame.mixer.Sound("./sound/Wood_dig3.mp3")]

woods = [pygame.image.load("./Textures/Bookshelf.webp"),
         pygame.image.load("./Textures/Oak_Planks.webp"),
         pygame.image.load("./Textures/Hay_Bale.webp"),
         pygame.image.load("./Textures/Pumpking_Light.webp"),
         pygame.image.load("./Textures/Carved_Pumpkin.webp"),]

woods_sound_idx = [2, 2, 0, 1, 1]

block_sound_idx = [1, 1, 1, 1, 1, 1, 1, 2, 1, 0, 1, 1]

trunk = [pygame.image.load("./Textures/Birch.webp"),
         pygame.image.load("./Textures/Oak.webp")]

redstone_lamp = [pygame.image.load("./Textures/Off_Redstone_Lamp.webp"),
                 pygame.image.load("./Textures/On_Redstone_Lamp.webp")]

fire = pygame.image.load("./Textures/Fire.webp")

trunk_sound_idx = [2, 2]

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

class Block():
    def __bool__(self):
        return True
    def sound(self):
        pass
    def draw(self):
        pass
    def update(self, x, y):
        pass
    def edge_x(self, x):
        return min(width - 1, max(0, x))
    def edge_y(self, y):
        return min(bottom - 1, max(top, y))

class Wood():
    def __init__(self):
        self.typ = random.randrange(len(woods))
        self.fire = Fire()
        self.on_fire = False

    def update(self, x, y):
        pass

    def edge_x(self, x):
        return min(width - 1, max(0, x))
    def edge_y(self, y):
        return min(bottom - 1, max(top, y))
    
    def draw(self, x, y, alpha = 255):
        image = woods[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
        if self.on_fire: 
            self.fire.draw(x, y)
    
    def sound(self):
        sounds[woods_sound_idx[self.typ]].play()

class Fire(Block):
    def __init__(self):
        self.frame = 0
        self.t = Timer(80, True)

    def __bool__(self):
        return False
    def sound(self):
        pass

    def update(self, x, y):
        b = self.edge_y(y + 1)
        if isinstance(m[b][x], Wood):
            m[b][x].on_fire = 1
        else:
            m[y][x] = 0

    def draw(self, x, y, alpha = 255):
        if self.t.check():
            self.frame = (self.frame + 1) % 32
            self.t.deactivate()
            self.t.activate()
        image = fire.subsurface((0, self.frame * 28 + 1), (28, 27))
        image.set_alpha(alpha)
        screen.blit(image, (x,y))

class Redstone_Lamp(Block):
    def __init__(self):
        self.state = 0
    
    def draw(self, x, y, alpha = 255):
        image = redstone_lamp[self.state]
        image.set_alpha(alpha)
        screen.blit(image, (x,y))

    def update(self, x, y):
        for i in range(4):
            a = self.edge_x(x + dx[i])
            b = self.edge_y(y + dy[i])
            if isinstance(m[b][a], Redstone):
                self.state = 1
                break

class Redstone(Block):    
    def draw(self, x, y, alpha = 255):
        image = pygame.image.load("./Textures/Redstone.webp")
        image.set_alpha(alpha)
        screen.blit(image, (x,y))

class Tnt(Block):
    def draw(self, x, y, alpha = 255):
        image = pygame.image.load("./Textures/TNT.webp")
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
    
    def sound(self):
        pygame.mixer.Sound("./sound/Grass_dig3.mp3").play()

class Blocks(Block):
    def __init__(self):
        self.typ = random.randrange(len(blocks))
    
    def draw(self, x, y, alpha = 255):
        image = blocks[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
    
    def sound(self):
        sounds[block_sound_idx[self.typ]].play()

class Tree(Wood):
    def __init__(self):
        self.on_fire = False
        self.fire = Fire()
        self.typ = random.randrange(len(trunk))
    
    def draw(self, x, y, alpha = 255):
        image = trunk[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
        if self.on_fire: 
            self.fire.draw(x, y)

    def sound(self):
        sounds[trunk_sound_idx[self.typ]].play()

typ = [Tnt, Blocks, Tree, Redstone, Redstone_Lamp, Fire, Wood]
weight = [0, 0, 0.4, 0, 0, 0.3, 0.3]
