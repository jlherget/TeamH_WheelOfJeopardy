import board
import wheel
import scoreboard
import pygame

class GameScreen():
    
    def __init__(self, app):
        self.app     = app
        self.board   = board.Board(app)
        self.wheel   = wheel.Wheel(app)
        self.scoreboard = scoreboard.Scoreboard(app)
        
    def Draw(self, screen):
        backgrounImage = pygame.image.load( "resources/background.jpg" )
        screen.blit( backgrounImage, (0, -150) )


        self.wheel.Draw( screen )
        self.board.Draw(screen)
        self.scoreboard.Draw(screen)


        
    def ProcessUiEvent(self, event):
        self.board.ProcessUiEvent(event)
        self.wheel.ProcessUiEvent(event)
        self.scoreboard.ProcessUiEvent(event)

    def startRound(self, round_num, round_qset):
        self.board.startRound(round_num, round_qset)