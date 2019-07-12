import board
import wheel

class GameScreen():
    
    def __init__(self, app):
        self.app     = app
        self.board   = board.Board(app)
        self.wheel   = wheel.Wheel(app)
        
    def Draw(self, screen):
        self.board.Draw(screen)
        self.wheel.Draw(screen)
        
    def ProcessUiEvent(self, event):
        self.board.ProcessUiEvent(event)
        self.wheel.ProcessUiEvent(event)