import pygame

# Define constants
# Define some colors
BLACK   = pygame.Color("black")
BLUE    = pygame.Color("blue")
GRAY    = pygame.Color("gray")
GREEN   = pygame.Color("green")
RED     = pygame.Color("red")
WHITE   = pygame.Color("white")
YELLOW  = pygame.Color("yellow")
PURPLE  = pygame.Color("purple")

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)

# General use button
class Button():

    def __init__(self, pos_x, pos_y, color, width, height, text):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = width
        self.height = height
        self.text   = text
        self.color  = color

    def Draw(self, screen, font_size, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.pos_x-2,self.pos_y-2,self.width+4,self.height+4),0)
        else:
            pygame.draw.rect(screen, self.color, (self.pos_x,self.pos_y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', font_size)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y + (self.height/2 - text.get_height()/2)))   

    def isHighlighted(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.pos_x and pos[0] < self.pos_x + self.width:
            if pos[1] > self.pos_y and pos[1] < self.pos_y + self.height:
                return True
        return False 
