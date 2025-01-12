import pygame
import random
import test
from copy import deepcopy
from basic import top, bottom, width, screen, clock, length, m, margin_l, music, init_map, heading, sub_heading, text
from bag_7 import Bag_7
from shape import pos
from rule import Rules

class Game():
    def __init__(self, music):
        pygame.mixer.Channel(0).play(random.choice(music))
        self.bag = Bag_7()
        self.rule = Rules()
        self.tetro = self.bag.get()
        self.tetro.speed_v = self.rule.speed

    def draw_interface(self, bag):
        ql = bag.hh
        for i in range(7):
            pygame.draw.rect(screen, 'black', pygame.Rect(335, i * 85 + 65, 130, 85), 1)

            pos_x = 375
            pos_y = i * 85 + 110
            name = bag.queue[ql].name
            state = bag.queue[ql].state
            box = bag.queue[ql].box
            for j in range(len(box)):
                box[j].draw(pos_x + pos[name][state][j][0] * (length - 2), pos_y + pos[name][state][j][1] * (length - 2))
            ql = (ql + 1) % 7

        screen.blit(heading.render("NEXT", False, 'white'), (360, 30))

    def draw_background(self):
        imp = pygame.image.load("./images/playgound.png")
        screen.blit(imp, (margin_l, 2 * length))

    def background_music(self, music):
        if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(random.choice(music))

    def inpt(self):
        d = pygame.key.get_pressed()
        if d[pygame.K_p]:
            self.pause()

    def restart(self):
        self.exp = pygame.mixer.Sound("./sound/Successful_hit.mp3")
        pygame.mixer.Channel(0).play(random.choice(music))
        self.bag = Bag_7()
        self.rule = Rules()
        self.tetro = self.bag.get()
        self.tetro.speed_v = self.rule.speed
        init_map()

    def pause(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit()
            key = pygame.key.get_pressed()
            
            text = sub_heading.render("Resume[E]   Restart[R]", False, 'white')
            screen.blit(text, (margin_l + 6,675))
            if key[pygame.K_e]:
                return
            elif key[pygame.K_r]:
                self.restart()
                return

            pygame.display.update()
            clock.tick()
            

    def draw(self):
        for i in range(top, bottom):
            for j in range(width):
                if isinstance(m[i][j], int) and m[i][j] == 1:
                    pygame.draw.rect(screen, 'red', (j * length + 1 + margin_l, (i - top + 2) * length + 1, 28, 28))
                elif m[i][j]:
                    m[i][j].draw(j * length + 1 + margin_l, (i - top + 2) * length + 1)

game = Game(music)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit()
    screen.fill((156,156,156))
    game.background_music(music)
    game.draw_interface(game.bag)
    game.draw_background()
    game.rule.draw_score()
    game.draw()
    game.tetro.pre_view()
    game.tetro.draw(255)
    if game.tetro.update():
        game.tetro = game.bag.get()
        game.tetro.speed_v = game.rule.speed

    game.inpt()
    game.tetro.iput()
    game.rule.update()

    if game.rule.is_over():
        game.restart()
    pygame.display.update()
    clock.tick()