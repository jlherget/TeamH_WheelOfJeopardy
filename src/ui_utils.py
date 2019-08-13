import pygame

SCREEN_WIDTH  = 900
SCREEN_HEIGHT = 700
SCREEN_SIZE   = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Define constants
# Define some colors
class Colors():
    BLACK   = pygame.Color("black")
    BLUE    = pygame.Color("blue")
    GRAY    = pygame.Color("gray")
    GREEN   = pygame.Color("green")
    RED     = pygame.Color("red")
    WHITE   = pygame.Color("white")
    YELLOW  = pygame.Color("yellow")
    PURPLE  = pygame.Color("purple")

# General use button
class Button():
    """General use button.

    Create a button that can be drawn at a given location with a given size and color.
    Button can display specified text as well.

    """

    def __init__(self, pos_x, pos_y, color, width, height, text):
        self.pos_x  = pos_x
        self.pos_y  = pos_y
        self.width  = width
        self.height = height
        self.text   = text
        self.color  = color

    def Draw(self, screen, font_size, outline=None):
        """Draw the button onto the screen using the given font size.
        
        Args:
            screen      - Pygame screen object to draw on.
            font_size   - Font size for the text to be dispalyed
            outline     - Outline color. Defaults to none.
        Return:
            None.
        
        """
        if outline:
            pygame.draw.rect(screen, outline, (self.pos_x-2,self.pos_y-2,self.width+4,self.height+4),0)
        else:
            pygame.draw.rect(screen, self.color, (self.pos_x,self.pos_y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('arial', font_size)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.pos_x + (self.width/2 - text.get_width()/2), self.pos_y + (self.height/2 - text.get_height()/2)))   

    def isHighlighted(self, pos):
        """Check if the mouse is hovered over the button.

        Args:
            pos - mouse position or a tuple of (x,y) coordinates
        Return:
            True if mouse position is over the button.

        """
        if pos[0] > self.pos_x and pos[0] < self.pos_x + self.width:
            if pos[1] > self.pos_y and pos[1] < self.pos_y + self.height:
                return True
        return False 
