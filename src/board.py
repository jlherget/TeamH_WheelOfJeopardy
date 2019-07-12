import pygame
import gameboard

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
        
    def Draw(self, screen):
        
        # Background for the questions
        boardRect = pygame.Rect([self.pos_x, self.pos_y, self.BOARD_WIDTH, self.BOARD_HEIGHT])
        pygame.draw.rect(screen, gameboard.BLUE, boardRect)
        
        #Top line
        pygame.draw.rect(screen, gameboard.BLACK, [self.pos_x, self.pos_y, self.BOARD_WIDTH, 5])
        
        # Categories
        for i in range(self.NUM_COLS+1):
            left    = self.pos_x + self.COL_WIDTH *i
            top     = self.pos_y
            width   = 5
            height  = self.ROW_HEIGHT
            pygame.draw.rect(screen, gameboard.BLACK, [left, top, width, height])
            
        # Categories/questions seaparator
        pygame.draw.rect(screen, gameboard.BLACK, [self.pos_x, self.pos_y + self.ROW_HEIGHT, self.BOARD_WIDTH + 5, self.SEPARATOR_HEIGHT])
        
        # Draw the lines between rows
        for i in range(self.NUM_QROWS+1):
            top     = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * i
            left    = self.pos_x
            width   = self.BOARD_WIDTH + 5
            height  = 5
            pygame.draw.rect(screen, gameboard.BLACK, [left, top, width, height])
             
        # Draw the lines between columns
        for i in range(self.NUM_COLS+1):
            top     = self.pos_y + self.QY_OFFSET 
            left    = self.pos_x + self.COL_WIDTH *i
            width   = 5
            height  = self.ROW_HEIGHT * self.NUM_QROWS
            pygame.draw.rect(screen, gameboard.BLACK, [left, top, width, height])
            
        # Draw the dollar amounts that havent been revelead
        font = pygame.font.SysFont('Calibri', 25, True, False)
        for r in range(self.NUM_QROWS):
            for c  in range(self.NUM_COLS):
                x = self.pos_x + self.COL_WIDTH*c + self.COL_WIDTH / 3
                y = self.pos_y + self.QY_OFFSET + self.ROW_HEIGHT * r + self.ROW_HEIGHT / 2.5
                s = '${}'.format((r+1) * self.BASE_VALUE)
                text = font.render(s, True, gameboard.YELLOW)
                screen.blit(text, [x, y])

class Board():
    def __init__(self, app):
        self.running = True
        self.app     = app
        self.ui      = QuestionsBoardUI(320, 0)

    def PostMessage(self, message):
        self.app.queue.put(message)
        
    def Draw(self, screen):
        self.ui.Draw(screen)
