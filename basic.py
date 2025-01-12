import pygame
pygame.init()
screen = pygame.display.set_mode((500, 800))
clock = pygame.time.Clock()
font = pygame.font.Font("./Minecraft.ttf", 30)
music = [pygame.mixer.Sound("./music/Haggstrom.mp3"),
         pygame.mixer.Sound("./music/Living_Mice.mp3"),
         pygame.mixer.Sound("./music/Minecraft.mp3"),
         pygame.mixer.Sound("./music/Subwoofer_Lullaby.mp3"),
         pygame.mixer.Sound("./music/Wet_Hands.mp3"),]

top = 10
bottom = 30
width = 10
length = 30
margin_l = 20

m = [[0 for i in range(10)] for j in range(30)]