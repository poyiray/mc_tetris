import pygame
import random
from srs import collision, collision_SRS
from timer import Timer
from copy import deepcopy
from shape import typ, pos, name
from basic import top, bottom, width, screen, clock, length, font, m
import test

class Grid():
    #消行
    def clear(self, arr):
        for i in range(len(arr)): arr[i] = 0
    
    def update(self):
        for i in range(top, bottom):
            f = True
            for j in range(width):
                #如果不是满行
                if not m[i][j]: 
                    f = False
                    break
            if f:
                #清除之后将上方的方格落下
                self.clear(m[i])
                for j in range(i - 1, top, -1):
                    m[j + 1] = deepcopy(m[j])
                self.clear(m[top])

    def draw_interface(self):
        pygame.draw.rect(screen, 'black', pygame.Rect(325, 60, 150, 600), 2)
        text = font.render("NEXT", True, 'white')
        screen.blit(text, (360, 30))

    def draw_backgound(self):
        imp = pygame.image.load("./images/playgound.png")#.convert()
        screen.blit(imp, (0, 2 * length))

    def draw(self):
        for i in range(top, bottom):
            for j in range(width):
                if isinstance(m[i][j], int) and m[i][j] == 1:
                    pygame.draw.rect(screen, 'red', (j * length + 1, (i - top + 2) * length + 1, 28, 28))
                elif m[i][j]:
                    m[i][j].draw(j * length + 1, (i - top + 2) * length + 1)

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

#Tetrominoes
class Tetro():
    t_s = Timer(250)
    def __init__(self, pos_x, pos_y):
        self.rule = Rules()
        self.speed_v = 1000
        self.t_h = Timer(100)
        self.t_v = Timer(self.speed_v) # 600
        self.t_r = Timer(240)

        self.pos_x = pos_x
        self.pos_y = pos_y
        
        self.name = random.choice(name)
        #self.name = "I"
        self.typ = random.choice(typ)()
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
            return self.rule.fixed(self.box, self.x, self.y) 

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
        self.draw(90, self.x, self.y_t);

    def draw(self, alpha, x, y):
        for i in range(len(x)):
            self.box[i].draw(x[i] * length + 1, (y[i] - top + 2) * length + 1, alpha)

tetro = Tetro(4,top - 2)
grid = Grid()
rule = Rules()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
    screen.fill("gray")

    key = pygame.key.get_pressed()
    grid.draw_interface()
    grid.draw_backgound()
    grid.draw()
    tetro.pre_view()
    tetro.draw(255, tetro.x, tetro.y)
    if tetro.update():
        del tetro
        tetro = Tetro(4,top - 2)
    tetro.iput()
    grid.update()

    if rule.is_over():
        exit()
    pygame.display.update()
    clock.tick()