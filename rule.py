import pygame
from copy import deepcopy
from basic import bottom, m, width, heading, sub_heading, text, screen, top
from timer import Timer

class Rules():
    def __init__(self):
        self.exp = pygame.mixer.Sound("./sound/Successful_hit.mp3")
        self.level_up = pygame.mixer.Sound("./sound/levelup.mp3")
        self.speed = 600
        self.score = 0
        self.t = Timer(800)

    #used to clear the line, set all the values to 0/empty
    def clear(self, arr):
        for i in range(len(arr)): arr[i] = 0
    
    def update(self):
        #call every blocks' update function
        for i in range(top, bottom):
            for j in range(width):
                if isinstance(m[i][j], int) and not m[i][j]: continue #if it is 0, then continue
                if not isinstance(m[i][j], int): #if it is a special block
                    m[i][j].update(j, i)

        #scan line by line to check if there exist a line that is full
        for i in range(top, bottom):
            f = True
            for j in range(width):
                if not m[i][j]: 
                    f = False
                    break
            if f: #if there xist a line that is full, the elimination will be performed 
                self.score += 10 #score will add up by 10

                #the sound effect for the elimination
                if not self.score % 100:
                    pygame.mixer.Channel(1).play(self.level_up)
                else:
                    pygame.mixer.Channel(1).play(self.exp)

                self.speed = max(100, self.speed - 3) #the speed will increase
                for j in range(i - 1, top - 1, -1): #the lines from the above will be shifted down
                    m[j + 1] = deepcopy(m[j])
                self.clear(m[top]) #clear the unnecessary line

    #used to print user's score
    def draw_score(self):
        screen.blit(sub_heading.render("SCORE", False, 'White'), (360,675))
        screen.blit(text.render(f"{self.score}", False, 'red'), (360, 700))

    def is_over(self):
        #if the blocks go over the top of the map, then the game is over, return True
        for i in range(0, 10):
            for j in range(0,10):
                if m[i][j]: return True
        return False
    
    def collision_v(self, x, y):
        #check if the tetromino will touches any blocks after moving down by one block
        for i in range(len(y)):
            if y[i] + 1 >= bottom or m[y[i] + 1][x[i]]:
                self.t.activate() #activate the timer
                return True
        self.t.deactivate() #if tetromino does not touch any blocks, deactivate the timer (restart the timer)
        return False

    def collision_h(self, x, y, d):
        #check if the tetromino will touches any blocks after moving to d direction by one block
        for i in range(len(x)):
            if x[i] + d < 0 or x[i] + d >= width or m[y[i]][x[i] + d]:
                return True
        return False
    
    def fixed(self, box, x, y):
        #fixed the tetromino, when the timer reaches certain time
        if not self.t.check(): return False

        for i in range(len(x)):
            m[y[i]][x[i]] = deepcopy(box[i])
        return True
