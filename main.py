import pygame
import random
from timer import Timer
from copy import copy, deepcopy
from shape import shape, color, name

pygame.init()
screen = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()
font = pygame.font.Font("Minecraft.ttf", 30)

#向下位移10格，预留一些位置
top = 10
bottom = 30
width = 10
length = 30

class Cell():
    def __init__(self, name = "empty", form = 0):
        self.name = name
        self.form = form

    def __bool__(self):
        return self.name != "empty"

m = [[Cell() for i in range(10)] for j in range(31)]

class Grid():
    #消行
    def clear(self, arr):
        for i in range(len(arr)): arr[i] = Cell()
    
    def update(self):
        for i in range(top, bottom + 1):
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
        imp = pygame.image.load("./images/playgound.png").convert()
        screen.blit(imp, (0, 2 * length))

    def draw(self):
        for i in range(top, bottom + 1):
            for j in range(width):
                if m[i][j]:
                    #画出一个正方形 其中包括方块的颜色，x轴y轴的位置，和长度宽度
                    pygame.draw.rect(screen, color[m[i][j].name], (j * length + 1, (i - top + 2) * length + 1, length - 2, length - 2))

class Rules():
    def __init__(self):
        self.t = Timer(800)

    def is_over(self):
        #上方如果堆积了方块就是越界了
        for i in range(0, 10):
            for j in range(0,10):
                if m[i][j]: return True
        return False
    
    def collision_v(self, struct, x, y, d = 1):
        for i in range(len(struct)):
            for j in range(len(struct[i])):
                if not struct[i][j]: continue;
                if y[i][j] + 1 >= bottom or m[y[i][j] + 1][x[i][j]]:
                    self.t.activate()
                    return True
        self.t.deactivate()
        return False

    def collision_h(self, struct, x, y, d):
        for i in range(len(struct)):
            for j in range(len(struct[i])):
                if not struct[i][j]: continue
                if x[i][j] + d < 0 or x[i][j] + d >= width: return True
                if m[y[i][j]][x[i][j] + d]: return True
        return False       
    
    def collision(self, struct, x, y):
        self.tmp_x = deepcopy(x)
        for i in range(len(struct)):
            for j in range(len(struct[i])):
                if not struct[i][j]: continue
                if x[i][j] < 0 or x[i][j] >= width: return True
                if y[i][j] < 0 or y[i][j] >= bottom: return True
                if m[y[i][j]][x[i][j]]: return True
        return False
    
    def fixed(self, struct, name, x, y):
        if not self.t.check(): return False
        self.t.deactivate()
        for i in range(len(struct)):
            for j in range(len(struct[i])):
                if struct[i][j]:
                    m[y[i][j]][x[i][j]] = Cell(name)
        return True

#Tetrominoes
class Tetro():
    t_s = Timer(250)
    queue = []
    def __init__(self, pos_x, pos_y):
        self.rule = Rules()
        self.speed_v = 400
        self.t_h = Timer(100)
        self.t_v = Timer(self.speed_v) # 600
        self.t_r = Timer(245)
        # T Z S J L I O
        self.name = random.choice(name)
        #self.name = 'I'

        #拿出对应的颜色 结构 并且构建一个方块数组，储存cell类
        self.struct = deepcopy(shape[self.name])
        self.color = deepcopy(color[self.name])
        self.x = deepcopy(self.struct)
        self.y = deepcopy(self.struct)
        self.y_t = deepcopy(self.y)

        for i in range(len(self.struct)):
            for j in range(len(self.struct[i])):
                self.x[i][j] = pos_x + j
                self.y[i][j] = pos_y + i - len(self.struct) + 1

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
        
        if self.rule.collision_v(self.struct, self.x, self.y): 
            return self.rule.fixed(self.struct, self.name, self.x, self.y) 

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
            self.y = deepcopy(self.y_t)
            self.rule.t.duration = 0
        elif(d[pygame.K_w]):
            self.t_v.duration = self.speed_v * 0.2
        elif(not d[pygame.K_w]):
            self.t_v.duration = self.speed_v

    def move_h(self, d):
        if self.rule.collision_h(self.struct, self.x, self.y, d): return
        self.x = [[val + d for val in row] for row in self.x]

    def move_v(self):
        if self.rule.collision_v(self.struct, self.x, self.y): return
        self.y = [[val + 1 for val in row] for row in self.y]

    def rotate(self, d):
        tmp = deepcopy(self.struct)
        
        for i in range(len(self.struct)):
            for j in range(i):
                self.struct[i][j], self.struct[j][i] = self.struct[j][i], self.struct[i][j];
        if d == -1: 
            self.struct = self.struct[::-1]
        elif d == 1:
            self.struct = [row[::-1] for row in self.struct]
        if rule.collision(self.struct, self.x, self.y):
            self.struct = deepcopy(tmp)

    def pre_view(self):
        self.y_t = deepcopy(self.y)
        while(not rule.collision(self.struct, self.x, self.y_t)):
            self.y_t = [[val + 1 for val in row] for row in self.y_t]
        self.y_t = [[val - 1 for val in row] for row in self.y_t]
        self.draw((190, 190, 190), 150, self.x, self.y_t);

    def draw(self, color, alpha, x, y):
        for i in range(len(self.struct)):
            for j in range(len(self.struct[i])):
                if(self.struct[i][j]):
                    s = pygame.Surface((length - 2, length - 2))
                    s.set_alpha(alpha)
                    s.fill(color)
                    screen.blit(s, (x[i][j] * length + 1, (y[i][j] - top + 2) * length + 1))
                   # pygame.draw.rect(screen, color, (x[i][j] * length + 1, (y[i][j] - top + 2) * length + 1, length - 2, length - 2))

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
    tetro.draw(tetro.color, 255, tetro.x, tetro.y)
    if tetro.update():
        del tetro
        tetro = Tetro(4,top - 2)
    tetro.iput()
    grid.update()

    if rule.is_over():
        exit()
    pygame.display.update()
    clock.tick()