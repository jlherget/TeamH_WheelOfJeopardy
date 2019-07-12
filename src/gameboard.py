import pygame
import math
import random
import messages
import wheel

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
SCREEN_HEIGHT = 600
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)
 
# The
class WheelUI():
    TRIANGLE_WIDTH  = 20
    TRIANGLE_HEIGHT = 15
        
    WHEEL_WIDTH  = 300
    WHEEL_HEIGHT = 300
    WHEEL_SIZE   = (WHEEL_WIDTH, WHEEL_HEIGHT)
    
    WHEEL_SPIN_ACC          = 0.02
    WHEEL_SPIN_ANG_VEL_INIT = -5
    
    def __init__(self, pos_x, pos_y, app):
        self.app = app
        self.pos_x          = pos_x
        self.pos_y          = pos_y
        self.angle          = 0
        self.angle_vel      = 0
        self.angle_acc      = 0
        self.prev_angle_vel = 0
        self.wheel_img      = self.CreateWheelSurface()
        self.img_rect       = self.wheel_img.get_rect(topleft=(self.pos_x, self.pos_y))
        
    def CreateWheelSurface(self):
        wheel_img       = pygame.image.load("resources/wheel.png").convert_alpha()
        wheel_img  = pygame.transform.scale(wheel_img, self.WHEEL_SIZE)
        return wheel_img
         

    def Spin(self):
        # Start spinning the wheel (if it's not already spinning)
        if self.angle_vel == 0:
            print("SPIN IN MESSAGE RECEIVED: SPINNING WHEEL")
            self.angle_vel = random.randrange(-10, -6)
        
    def Draw(self, screen):
        # If the wheel is spinning, update the image angle
        if self.angle_vel != 0:
            self.angle           += self.angle_vel
            self.prev_angle_vel   = self.angle_vel
            self.angle_vel       += self.WHEEL_SPIN_ACC + random.randrange(0, 1)/10000
            
            # Check if the wheel has stopped (i.e. velocity sign changes)
            if self.angle_vel == 0 or math.copysign(self.angle_vel, self.prev_angle_vel) != self.angle_vel:
                # At this point, we would send a message back to the app
                # with the result.
                self.angle_vel = 0
                print("SPIN COMPLETED, SENDING OUTPUT TO MAIN")
                self.app.wheel_screen.PostMessage(messages.SpinOutMessage(6))
            self.angle %= 360
        
        rot_image = pygame.transform.rotate(self.wheel_img, self.angle)
    
        # Copy image to screen:
        self.img_rect = rot_image.get_rect(center=self.img_rect.center)
        screen.blit(rot_image, self.img_rect)
        
        # Draw little triangle at the top
        triangle_p1 = (self.pos_x + self.WHEEL_WIDTH / 2 - self.TRIANGLE_WIDTH / 2, 
                       self.pos_y)
        triangle_p2 = (triangle_p1[0] + self.TRIANGLE_WIDTH / 2, 
                       triangle_p1[1] + self.TRIANGLE_HEIGHT)
        triangle_p3 = (triangle_p1[0] + self.TRIANGLE_WIDTH, self.pos_y)
        triangle_points = [triangle_p1, triangle_p2, triangle_p3]
        
        pygame.draw.polygon(screen, GREEN, triangle_points)
        
class QuestionsBoardUI():
    NUM_COLS   = 6
    NUM_QROWS  = 5 # Not including categories row
    ROW_HEIGHT = 70
    COL_WIDTH  = 90
    COL_LINE_WIDTH = 4
    ROW_LINE_WIDTH = 4
    SEPARATOR_HEIGHT = 15
    
    QY_OFFSET = ROW_HEIGHT + SEPARATOR_HEIGHT
    
    BOARD_WIDTH   = COL_WIDTH * NUM_COLS
    BOARD_HEIGHT  = ROW_HEIGHT * (NUM_QROWS+1) + SEPARATOR_HEIGHT
    
    BASE_VALUE  = 200
    
    
    def __init__(self, pos_x, pos_y):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        
    def Draw(self, screen, wheelTurn):
        
        # Background for the questions
        boardRect = pygame.Rect([self.pos_x, self.pos_y, self.BOARD_WIDTH, self.BOARD_HEIGHT])
        if wheelTurn:
            pygame.draw.rect(screen, BLUE, boardRect)
        else:
            pygame.draw.rect(screen, GREEN, boardRect) 
        #Top line
        pygame.draw.rect(screen, BLACK, [self.pos_x, self.pos_y, self.BOARD_WIDTH, 5])
        
        # Categories
        for i in range(self.NUM_COLS+1):
            left    = self.pos_x + self.COL_WIDTH *i
            top     = self.pos_y
            width   = 5
            height  = self.ROW_HEIGHT
            pygame.draw.rect(screen, BLACK, [left, top, width, height])
            
        # Categories/questions seaparator
        pygame.draw.rect(screen, BLACK, [self.pos_x, self.pos_y + self.ROW_HEIGHT, self.BOARD_WIDTH + 5, self.SEPARATOR_HEIGHT])
        
        # Draw the lines between rows
        for i in range(self.NUM_QROWS+1):
            top     = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * i
            left    = self.pos_x
            width   = self.BOARD_WIDTH + 5
            height  = 5
            pygame.draw.rect(screen, BLACK, [left, top, width, height])
             
        # Draw the lines between columns
        for i in range(self.NUM_COLS+1):
            top     = self.pos_y + self.QY_OFFSET 
            left    = self.pos_x + self.COL_WIDTH *i
            width   = 5
            height  = self.ROW_HEIGHT * self.NUM_QROWS
            pygame.draw.rect(screen, BLACK, [left, top, width, height])
            
        # Draw the dollar amounts that havent been revelead
        font = pygame.font.SysFont('Calibri', 25, True, False)
        for r in range(self.NUM_QROWS):
            for c  in range(self.NUM_COLS):
                x = self.pos_x + self.COL_WIDTH*c + self.COL_WIDTH / 3
                y = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * r + self.ROW_HEIGHT / 2.5
                s = '${}'.format((r+1) * self.BASE_VALUE)
                text = font.render(s, True, YELLOW)
                screen.blit(text, [x, y])

class StartButtonUI():
    def __init__(self, pos_x, pos_y, color, width, height, text):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def Draw(self, screen, font_size, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.pos_x-2,self.pos_y-2,self.width+4,self.height+4),0)
        else:
            pygame.draw.rect(screen, self.color, (self.pos_x,self.pos_y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('ariel', font_size)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y + (self.height/2 - text.get_height()/2)))   

    def isHighlighted(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.pos_x and pos[0] < self.pos_x + self.width:
            if pos[1] > self.pos_y and pos[1] < self.pos_y + self.height:
                return True        
        return False         
