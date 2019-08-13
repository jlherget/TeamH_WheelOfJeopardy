import board
import wheel
import scoreboard

class GameScreen():
    """Facade class to store the Board, Wheel, and Scoreboard classes."""
    
    def __init__(self, app):
        self.app     = app
        self.board   = board.Board(app)
        self.wheel   = wheel.Wheel(app)
        self.scoreboard = scoreboard.Scoreboard(app)
        
    def Draw(self, screen):
        """Draw the Board, Wheel, and Scoreboard onto the pygame screen."""
        self.board.Draw(screen)
        self.wheel.Draw(screen)
        self.scoreboard.Draw(screen)
        
    def ProcessUiEvent(self, event):
        """Allow the Board, Wheel, and Scoreboard to process user interface events."""
        self.board.ProcessUiEvent(event)
        self.wheel.ProcessUiEvent(event)
        self.scoreboard.ProcessUiEvent(event)

    def startRound(self, round_num, round_qset):
        """Start the round.

        Initializes the board with the next set of questions and answers.

        Args:
            round_num  - The round number. Integer. Range: [1,2]
            round_qset - RoundSet object for the round.
        Return:
            None.
        """
        self.board.startRound(round_num, round_qset)