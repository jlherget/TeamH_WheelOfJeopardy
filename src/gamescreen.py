import board
import wheel
import scoreboard

class GameScreen():
    
    def __init__(self, app):
        self.app     = app
        self.board   = board.Board(app)
        self.wheel   = wheel.Wheel(app)
        self.scoreboard = scoreboard.Scoreboard(app)
        
    def Draw(self, screen):
        self.board.Draw(screen)
        self.wheel.Draw(screen)
        self.scoreboard.Draw(screen)
        
    def ProcessUiEvent(self, event):
        self.board.ProcessUiEvent(event)
        self.wheel.ProcessUiEvent(event)
        self.scoreboard.ProcessUiEvent(event)