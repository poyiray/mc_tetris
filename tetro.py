import pygame
from timer import Timer
from rule import Rules
from copy import deepcopy
from shape import pos, Fire
from basic import length, top, margin_l
from srs import collision, collision_SRS

#Tetrominoes
class Tetro():
    t_s = Timer(250) #timer for the key 's'

    #requires the info, which is the shape and the type
    #and the central point of the tetromino
    def __init__(self, info, pos_x, pos_y):
        self.rule = Rules() #this is used to check collision
        self.speed_v = 600 #the initial vertical speed
        self.t_h = Timer(105) #the timer for the key 'h'
        self.t_v = Timer(self.speed_v) #the timer for the vertical movement
        self.t_r = Timer(240) #the timer for rotation

        #central point (pos_x, pos_y)
        self.pos_x = pos_x
        self.pos_y = pos_y
        
        #get the information about the shape and the type
        self.name = info[0]
        #self.name = "I"
        self.typ = info[1]() 
        #self.typ = Fire()

        self.state = 0 #the inital state is 0, indicating there was no rotation
        self.x = [] #store the x location for each blocks
        self.y = [] #store the y location for each blocks
        self.box = [] #store the objects of each blocks
        
        #add the objects of each blocks into the list (box)
        for i in range(4):
            self.box.append(deepcopy(self.typ))

        #offset by the center point to get x and y
        for i in range(4):
            self.x.append(pos_x + pos[self.name][self.state][i][0])
            self.y.append(pos_y + pos[self.name][self.state][i][1])

        self.y_t = deepcopy(self.y) #this stores the y location for the teromino's pre_view

    def update(self):
        #if the timer is not activated, then the tetromino will move down by one block, and then the timer will be activated
        if not self.t_v.active:
            self.move_v()
            self.t_v.activate()
        
        #update the timers
        if Tetro.t_s.check():
            Tetro.t_s.deactivate()
        if self.t_v.check():
            self.t_v.deactivate()
        if self.t_h.check():
            self.t_h.deactivate()
        if self.t_r.check():
            self.t_r.deactivate()
        
        #if the tetromino can no longer move
        if self.rule.collision_v(self.x, self.y): 
            #if the tetromino can be fixed
            if self.rule.fixed(self.box, self.x, self.y):
                #the sound of the blocks will be played, and then return True
                self.sound()
                return True
        
    def sound(self):
        #play the sound for each blocks
        for i in self.box: i.sound()

    def iput(self):
        d = pygame.key.get_pressed()

        #if user inputed d or a and the timer for horizontal movement is not activated, perform horizontal move, and then activate the timer
        if(d[pygame.K_d] - d[pygame.K_a]) and not self.t_h.active:
            self.move_h(d[pygame.K_d] - d[pygame.K_a])
            self.t_h.activate()
        
        #if user inputed left or right and the timer for rotation is not activated, perform rotation, and then activate the timer
        elif(d[pygame.K_RIGHT] - d[pygame.K_LEFT]) and not self.t_r.active:
            self.rotate(d[pygame.K_RIGHT] - d[pygame.K_LEFT])
            self.t_r.activate()

        #if user inputed s and the timer for the key s is not activated, drop down the tetromino immediately, and then activate the timer
        elif(d[pygame.K_s] and not Tetro.t_s.active):
            self.y = self.y_t
            self.rule.t.duration = 0 #set this to zero, because I want it to be fixed immediately
            Tetro.t_s.activate()

        #if user pressed w, the tetromino will speed up
        elif(d[pygame.K_w]):
            self.t_v.duration = self.speed_v * 0.2

        #if user is not pressing the w, then reset the speed
        elif(not d[pygame.K_w]):
            self.t_v.duration = self.speed_v

    def move_h(self, d):
        #check if the tetromino will touches any blocks after moving to d direction by one block
        #if it is True, just return
        if self.rule.collision_h(self.x, self.y, d): return

        #the x location of central point and all the value in list(self.x) += d
        # -1 = left, 1 = right
        self.pos_x += d
        self.x = [val + d for val in self.x]

    def move_v(self):
        #check if the tetromino will touches any blocks after moving down by one block
        #if it is True, just return
        if self.rule.collision_v(self.x, self.y): return

        #the y location of central point and all the value in list(self.y) += 1
        self.pos_y += 1
        self.y = [val + 1 for val in self.y]

    def rotate(self, d):
        #perform rotation
        if self.name != 'O':
            collision_SRS(self, d)

    #draw the pre_view of the tetromino
    def pre_view(self):
        self.y_t = self.y
        # y locations for the pre_view of the tetromino continue to add up by 1, until it collide with other blocks.
        while(not collision(self.x, self.y_t)):
            self.y_t = [val + 1 for val in self.y_t]
        self.y_t = [val - 1 for val in self.y_t] # then all values -= 1

        #draw the pre_view 
        for i in range(len(self.x)):
            self.box[i].draw(self.x[i] * length + 1 + margin_l, (self.y_t[i] - top + 2) * length + 1, 115)

    #used to draw the tetromino
    def draw(self, alpha):
        for i in range(len(self.x)):
            self.box[i].draw(self.x[i] * length + 1 + margin_l, (self.y[i] - top + 2) * length + 1, alpha)