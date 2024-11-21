import pygame
class Timer():
    def __init__(self, duration, f = False):
        self.duration = duration
        self.start_time = 0
        self.active = f
    
    def activate(self):
        self.active = True
        self.start_time = pygame.time.get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0

    def check(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time >= self.duration and self.active:
            return True
        return False