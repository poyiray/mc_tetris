import pygame
import random
from timer import Timer
from basic import m, screen, top, bottom, width
#shape of the tetromino
name = ['I', 'T', 'J', 'O', 'Z', 'S', 'L']

#the offset information for every shape and their rotations 
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

#the images for blocks
blocks = [pygame.image.load("./Textures/Stone.webp"),
          pygame.image.load("./Textures/Block_of_Diamond.webp"),
          pygame.image.load("./Textures/Block_of_Iron.webp"),
          pygame.image.load("./Textures/Diamond_Ore.webp"),
          pygame.image.load("./Textures/Iron_Ore.webp"),
          pygame.image.load("./Textures/Coal_Ore.webp"),
          pygame.image.load("./Textures/Cobblestone.webp"),
          pygame.image.load("./Textures/Glowstone.webp"),
          pygame.image.load("./Textures/Grass_Block.webp"),
          pygame.image.load("./Textures/Off_Furnace.webp"),
          pygame.image.load("./Textures/On_Furnace.webp")]

#the images for woods
woods = [pygame.image.load("./Textures/Bookshelf.webp"),
         pygame.image.load("./Textures/Oak_Planks.webp"),
         pygame.image.load("./Textures/Hay_Bale.webp"),
         pygame.image.load("./Textures/Pumpking_Light.webp"),
         pygame.image.load("./Textures/Carved_Pumpkin.webp"),
         pygame.image.load("./Textures/Crafting_Table.webp")]

#the images for trunk
trunk = [pygame.image.load("./Textures/Birch.webp"),
         pygame.image.load("./Textures/Oak.webp")]

#the images for redstone_lamp
redstone_lamp = [pygame.image.load("./Textures/Off_Redstone_Lamp.webp"),
                 pygame.image.load("./Textures/On_Redstone_Lamp.webp")]

#the image for fire
fire = pygame.image.load("./Textures/Fire.webp")

#the sound effects
sounds = [pygame.mixer.Sound("./sound/Grass_dig3.mp3"),
               pygame.mixer.Sound("./sound/Metal_dig3.mp3"),
               pygame.mixer.Sound("./sound/Wood_dig3.mp3")]

#the index here indicates the sound effect correspoding to each block
#(need improvement here)
woods_sound_idx = [2, 2, 0, 1, 1, 2]
block_sound_idx = [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
trunk_sound_idx = [2, 2]

#(up, left, down, right)
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

#Boundary check
#A better solution might be to reserve a space for the boundary so that no boundary check is required.
def edge_x(x):
    return min(width - 1, max(0, x))
def edge_y(y):
    return min(bottom - 1, max(top, y))


#all blocks should have functions (sound draw update)
class Block():
    def __bool__(self):
        return True
    def sound(self):
        pass
    def draw(self):
        pass
    def update(self, x, y):
        pass 

class Wood():
    def __init__(self):
        self.typ = random.randrange(len(woods)) #randomly choose a type of wood
        self.fire = Fire() #used for displaying the fire animation
        self.t_fire = Timer(1300) #the spread speed of the fire
        self.on_fire = False #if the wood is on fire

    def update(self, x, y):
        f = False #if there are fire or wood that is on fire around this block
        for i in range(4):
            a = edge_x(x + dx[i])
            b = edge_y(y + dy[i])
            if isinstance(m[b][a], Wood) and m[b][a].on_fire or isinstance(m[b][a], Fire):
                f = True
                break
        
        #if the block is on fire or there is fire around the block, than start the timer
        #if not then turn off the timer (restart the timer)
        if self.on_fire or f:
            self.t_fire.activate()
        else:
            self.t_fire.deactivate()

        #after a period of time
        if self.t_fire.check():
            if self.on_fire: #if it is already on fire, then it is burned out
                m[y][x] = 0
            self.on_fire = True #it is on fire
            self.t_fire.deactivate() #restart the timer

    #print the image
    def draw(self, x, y, alpha = 255):
        image = woods[self.typ]
        image.set_alpha(alpha) #Set the transparency of the image
        screen.blit(image, (x, y)) #print the image
        if self.on_fire: #if it is on fire, then print the fire animation
            self.fire.draw(x, y)
    
    def sound(self):
        sounds[woods_sound_idx[self.typ]].play() #play the sound of the block

#same as wood
#might need to simplify the code, reduce the repetition
class Tree(Wood):
    def __init__(self):
        self.on_fire = False
        self.fire = Fire()
        self.t_fire = Timer(1600)
        self.typ = random.randrange(len(trunk))
    
    def draw(self, x, y, alpha = 255):
        image = trunk[self.typ]
        image.set_alpha(alpha)
        screen.blit(image, (x, y))
        if self.on_fire: 
            self.fire.draw(x, y)

    def sound(self):
        sounds[trunk_sound_idx[self.typ]].play()

class Fire(Block):
    def __init__(self):
        self.frame = 0
        self.t = Timer(80, True) #the speed of the animation

    def __bool__(self):
        return False #can be used for elimination

    def update(self, x, y):
        b = edge_y(y + 1)
        #it can only stay on the top of the wood
        if not isinstance(m[b][x], Wood):
            m[y][x] = 0

    def draw(self, x, y, alpha = 255):
        if self.t.check():
            self.frame = (self.frame + 1) % 32
            #restart the timer
            self.t.deactivate()
            self.t.activate()
        
        image = fire.subsurface((0, self.frame * 28 + 1), (28, 27)) #find the image for each frame
        image.set_alpha(alpha)
        screen.blit(image, (x,y))

class Redstone_Lamp(Block):
    def __init__(self):
        self.state = 0 #it is on or off
    
    def draw(self, x, y, alpha = 255):
        image = redstone_lamp[self.state]
        image.set_alpha(alpha)
        screen.blit(image, (x,y))

    def update(self, x, y):
        #if there are redstones around this block, then it will be turned on
        for i in range(4):
            a = edge_x(x + dx[i])
            b = edge_y(y + dy[i])
            if isinstance(m[b][a], Redstone):
                self.state = 1
                break
    
    def sound(self):
        pygame.mixer.Sound("./sound/Metal_dig3.mp3").play()

class Redstone(Block):    
    def draw(self, x, y, alpha = 255):
        image = pygame.image.load("./Textures/Redstone.webp")
        image.set_alpha(alpha)
        screen.blit(image, (x,y))
        
    def sound(self):
        pygame.mixer.Sound("./sound/Metal_dig3.mp3").play()

#I wanted to add the TNT explosion effect, but I really couldn't find the TNT explosion animation, so I had to give it up for now.
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

class Sand(Block):
    def __init__(self):
        self.t_v = Timer(500) #the timer for vertical movement

    def draw(self, x, y, alpha = 255):
        image = pygame.image.load("./Textures/Sand.webp")
        image.set_alpha(alpha)
        screen.blit(image, (x, y))

    def update_d(self):
        #start the timer
        if not self.t_v.active:
            self.t_v.activate()
            self.f = True

        #after some time, stop the timer
        if self.t_v.check():
            self.t_v.deactivate()
    
    def update(self, x, y):
        b = edge_y(y + 1)

        #if there is a block underneath the sand, that means it can't fall, so just return
        if m[b][x]: return

        self.update_d() #update the timer

        #if the timer is off, then the reset the timer
        if not self.t_v.active:
            m[b][x] = m[y][x]
            m[y][x] = 0
            self.t_v.activate()

    def sound(self):
        pygame.mixer.Sound("./sound/Cherry_wood.mp3").play()

#all classes will be stored in the list (typ)
typ = [Tnt, Blocks, Tree, Redstone, Redstone_Lamp, Fire, Wood, Sand]
weight = [0.5,4,1,1,1,0.5,1,1] #the probability of getting each type of block, and not quite sure how it works, but the higher the number, the higher probability