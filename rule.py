import pygame
from copy import deepcopy
from basic import bottom, m, width, heading, sub_heading, text, screen, top
from timer import Timer

class Rules():
    def __init__(self):
        self.exp = pygame.mixer.Sound("./sound/Successful_hit.mp3")
        self.speed = 600
        self.score = 0
        self.t = Timer(800)

    def clear(self, arr):
        for i in range(len(arr)): arr[i] = 0
    
    def update(self):
        for i in range(top, bottom):
            for j in range(width):
                if isinstance(m[i][j], int) and not m[i][j]: continue
                if not isinstance(m[i][j], int):
                    m[i][j].update(j, i)

        for i in range(top, bottom):
            f = True
            for j in range(width):
                if not m[i][j]: 
                    f = False
                    break
            if f:
                pygame.mixer.Channel(1).play(self.exp)
                self.score += 10
                self.speed -= 3
                for j in range(i - 1, top - 1, -1):
                    m[j + 1] = deepcopy(m[j])
                self.clear(m[top])

    def draw_score(self):
        screen.blit(sub_heading.render("SCORE", False, 'White'), (360,675))
        screen.blit(text.render(f"{self.score}", False, 'red'), (360, 700))

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
