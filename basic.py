import pygame
pygame.init()
screen = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()
font = pygame.font.Font("./Minecraft.ttf", 30)

top = 10
bottom = 30
width = 10
length = 30

m = [[0 for i in range(10)] for j in range(30)]