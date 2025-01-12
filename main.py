import pygame
import random
import test
from copy import deepcopy
from basic import top, bottom, width, screen, clock, length, font, m, margin_l, music
from bag_7 import Bag_7
from shape import pos
from rule import Rules


class Game():
    def __init__(self, music):
        self.exp = pygame.mixer.Sound("./sound/Successful_hit.mp3")
        pygame.mixer.Channel(0).play(random.choice(music))

    def clear(self, arr):
        for i in range(len(arr)): arr[i] = 0
    
    def update(self):
        for i in range(top, bottom):
            f = True
            for j in range(width):
                if not m[i][j]: 
                    f = False
                    break
            if f:
                for j in range(i - 1, top - 1, -1):
                    m[j + 1] = deepcopy(m[j])
                self.clear(m[top])
                self.exp.play()

    def draw_interface(self, bag):
        ql = bag.hh
        for i in range(7):
            pygame.draw.rect(screen, 'black', pygame.Rect(335, i * 85 + 65, 130, 85), 1)

            pos_x = 375
            pos_y = i * 85 + 100
            name = bag.queue[ql].name
            state = bag.queue[ql].state
            box = bag.queue[ql].box
            for j in range(len(box)):
                box[j].draw(pos_x + pos[name][state][j][0] * (length - 2), pos_y + pos[name][state][j][1] * (length - 2))
            ql = (ql + 1) % 7

        text = font.render("NEXT", True, 'white')
        screen.blit(text, (360, 30))

    def draw_background(self):
        imp = pygame.image.load("./images/playgound.png")
        screen.blit(imp, (margin_l, 2 * length))

    def background_music(self, music):
        if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(random.choice(music))

    def draw(self):
        for i in range(top, bottom):
            for j in range(width):
                if isinstance(m[i][j], int) and m[i][j] == 1:
                    pygame.draw.rect(screen, 'red', (j * length + 1 + margin_l, (i - top + 2) * length + 1, 28, 28))
                elif m[i][j]:
                    m[i][j].draw(j * length + 1 + margin_l, (i - top + 2) * length + 1)

bag = Bag_7()
rule = Rules()
game = Game(music)
tetro = bag.get()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: exit()
    screen.fill((156,156,156))
    game.background_music(music)
    key = pygame.key.get_pressed()
    game.draw_interface(bag)
    game.draw_background()
    game.draw()
    tetro.pre_view()
    tetro.draw(255, tetro.x, tetro.y)
    if tetro.update():
        tetro = bag.get()
    tetro.iput()
    game.update()

    if rule.is_over():
        exit()
    pygame.display.update()
    clock.tick()