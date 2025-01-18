#import any required modules, variables, functions
import pygame
import random
import test #only used for testing
from basic import top, bottom, width, screen, length, m, margin_l, music, init_map, heading, sub_heading
from bag_7 import Bag_7
from shape import pos
from rule import Rules

#Game class is responsible for composing various classes, and drawing interfaces, and maps.
class Game():
    def __init__(self, music):
        #choice a background music at random
        pygame.mixer.Channel(0).play(random.choice(music))

        #Instantiating classes
        self.music = music
        self.bag = Bag_7()
        self.rule = Rules()
        self.tetro = self.bag.get() #get a tetromino from the 'bag'
        self.tetro.speed_v = self.rule.speed #change the speed of the tetromino

    #draw the interface (a list of upcoming tetrominoes, and user's score) on the screen
    def draw_interface(self):
        self.rule.draw_score() #draw users' score

        ql = self.bag.hh #ql is index of the left end of the queue
        for i in range(7):
            pygame.draw.rect(screen, 'black', pygame.Rect(335, i * 85 + 65, 130, 85), 1) #draw seven box on the right side of the screen

            pos_x = 375 #central point of the tetromino (pos_x, pos_y)
            pos_y = i * 85 + 110 #each tetrominoes are 85 units away from each other

            #get the shape(I O J L Z S T), state, and type of tetrominoes
            name = self.bag.queue[ql].name
            state = self.bag.queue[ql].state
            box = self.bag.queue[ql].box

            #in the box list, there stores the the objects of different types of blocks.
            for j in range(len(box)):
                #Draw differnet pictures according to the types of blocks
                box[j].draw(pos_x + pos[name][state][j][0] * (length - 2), pos_y + pos[name][state][j][1] * (length - 2))
            ql = (ql + 1) % 7 #head of the queue pops out the queue

        screen.blit(heading.render("NEXT", False, 'white'), (360, 30)) #print the text "NEXT"

    #this funtion is used to draw the playround of the game
    def draw_background(self):
        imp = pygame.image.load("./images/playgound.png")
        screen.blit(imp, (margin_l, 2 * length)) # print the playground image on the screen

    #this funtion is used to play the background music
    def background_music(self, music):
        #if the background music is not playing or has ended, then it will choose a background music from the list at random to play 
        if not pygame.mixer.Channel(0).get_busy():
            pygame.mixer.Channel(0).play(random.choice(self.music))

    #used to get the input from the user
    def inpt(self):
        #if the user pressed 'p', then the function pause will be called
        d = pygame.key.get_pressed()
        if d[pygame.K_p]:
            self.pause()

    #used to reset the game
    def restart(self):
        
        #choose a background music at random to play
        pygame.mixer.Channel(0).play(random.choice(self.music))
        self.bag = Bag_7() #regenerate the 7 bag
        self.rule = Rules() #Instantiate the Rules class
        self.tetro = self.bag.get() #get a tetromino from the queue
        self.tetro.speed_v = self.rule.speed #set the speed of the tetromino ot self.rule.speed
        init_map() #set all the values in the map to zero/empty

    #to pause the game, then print the interface that ask users if they want to continue or restart
    def pause(self):
        run = True
        while run:
            key = pygame.key.get_pressed() #user input
            text = sub_heading.render("Resume[E]   Restart[R]", False, 'white') 
            screen.blit(text, (margin_l + 6,675)) #print the text "Resume[E]" and "Restart[R]" on the screen
            
            #if user pressed 'e' then return back to the game
            #if user pressed 'r' then reset the game then exit the loop
            if key[pygame.K_e]:
                return
            elif key[pygame.K_r]:
                self.restart()
                return

            pygame.display.update() #used to update the game's graphics 
            #clock.tick()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT: run = False


    #used to draw the blocks that already exist on the map
    def draw(self):
        #here it starts from the top = 10 to bottom = 30, because I left some space on the top of the map.
        for i in range(top, bottom):
            for j in range(width): #loop through each values in this line
                if isinstance(m[i][j], int) and not m[i][j]: continue #is it is an int and 0, this means it is a empty space, just continue
                if isinstance(m[i][j], int) and m[i][j] == 1: # this is used for debugging. If it is an int and 1, print a red square
                    pygame.draw.rect(screen, 'red', (j * length + 1 + margin_l, (i - top + 2) * length + 1, 28, 28))
                else:
                    #if it is not an int, then draw the image, according to the type of the block. 
                    m[i][j].draw(j * length + 1 + margin_l, (i - top + 2) * length + 1) 

game = Game(music) #instantiate the Game class

#main loop of the game
run = True
while run:
    screen.fill((153,153,153)) #print the background color
    game.background_music(music) #play the background music
    game.draw_interface() #draw the interface
    game.draw_background() #print the background image
    game.draw() #print the images for the objects that already exist on the map
    game.tetro.pre_view() #print the pre_view of the tetromino, the one that player is controlling
    game.tetro.draw(255) #Draw the tetromino, and it must be behind the pre_view function, because otherwise the pre_view of the tetromino will stay on top of it.
    if game.tetro.update(): #the tetromino will move down by one block, then it will return True if tetromino can no longer move
        game.tetro = game.bag.get() #get a tetromino from the queue
        game.tetro.speed_v = game.rule.speed #reset the speed of the tetromino

    #deal with user's inputs
    game.inpt()
    game.tetro.iput()

    #this function will check if there is a line that is full. If yes, then elimination will be performed.
    game.rule.update()

    #check if the game is over.
    if game.rule.is_over():
        #if the game is over, then restart the game
        game.restart()

    pygame.display.update() #update the game's graphics
    #clock.tick() #I think it is used to set a particular FPS for the game to run at, but i'm not sure. Even I don't add this line the game still works perfectly fine.

    for event in pygame.event.get():
        if event.type == pygame.QUIT: run = False