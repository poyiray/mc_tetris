import pygame
from timer import Timer
from rule import Rules
from copy import deepcopy
from shape import pos
from basic import length, top, margin_l
from srs import collision, collision_SRS
#Tetrominoes
class Tetro():
    t_s = Timer(250)
    def __init__(self, info, pos_x, pos_y):
        self.rule = Rules()
        self.speed_v = 500
        self.t_h = Timer(100)
        self.t_v = Timer(self.speed_v) # 600
        self.t_r = Timer(240)

        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.name = info[0]
        #self.name = "S"
        self.typ = info[1]()
        self.state = 0
        self.x = []
        self.y = []
        self.box = []
        
        for i in range(4):
            self.box.append(deepcopy(self.typ))

        for i in range(4):
            self.x.append(pos_x + pos[self.name][self.state][i][0])
            self.y.append(pos_y + pos[self.name][self.state][i][1])
        self.y_t = deepcopy(self.y)

    def update(self):
        if not self.t_v.active:
            self.move_v()
            self.t_v.activate()
        
        if Tetro.t_s.check():
            Tetro.t_s.deactivate()
        if self.t_v.check():
            self.t_v.deactivate()
        if self.t_h.check():
            self.t_h.deactivate()
        if self.t_r.check():
            self.t_r.deactivate()
        
        if self.rule.collision_v(self.x, self.y): 
            if self.rule.fixed(self.box, self.x, self.y):
                self.sound()
                return True
        
    def sound(self):
        for i in self.box: i.sound()

    def iput(self):
        d = pygame.key.get_pressed()

        if(d[pygame.K_d] - d[pygame.K_a]) and not self.t_h.active:
            self.move_h(d[pygame.K_d] - d[pygame.K_a])
            self.t_h.activate()
        elif(d[pygame.K_RIGHT] - d[pygame.K_LEFT]) and not self.t_r.active:
            self.rotate(d[pygame.K_RIGHT] - d[pygame.K_LEFT])
            self.t_r.activate()
        elif(d[pygame.K_s] and not Tetro.t_s.active):
            Tetro.t_s.activate()
            self.y = self.y_t
            self.rule.t.duration = 0
        elif(d[pygame.K_w]):
            self.t_v.duration = self.speed_v * 0.2
        elif(not d[pygame.K_w]):
            self.t_v.duration = self.speed_v

    def move_h(self, d):
        if self.rule.collision_h(self.x, self.y, d): return
        self.pos_x += d
        self.x = [val + d for val in self.x]

    def move_v(self):
        if self.rule.collision_v(self.x, self.y): return
        self.pos_y += 1
        self.y = [val + 1 for val in self.y]

    def rotate(self, d):
        if self.name != 'O':
            collision_SRS(self, d)

    def pre_view(self):
        self.y_t = self.y
        while(not collision(self.x, self.y_t)):
            self.y_t = [val + 1 for val in self.y_t]
        self.y_t = [val - 1 for val in self.y_t]
        self.draw(115, self.x, self.y_t);

    def draw(self, alpha, x, y):
        for i in range(len(x)):
            self.box[i].draw(x[i] * length + 1 + margin_l, (y[i] - top + 2) * length + 1, alpha)