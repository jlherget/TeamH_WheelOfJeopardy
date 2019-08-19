class Player():
    """Hold player information."""

    def __init__(self):
        self.playerTokenCount  = 0          # Number of free spin tokens available.
        self.playerRoundScore  = [0,0]      # Player's score for each round
        self.roundNum          = 0          # Current round number (0-origin)

    def doubleScore(self):
        """Double the player's score for the current round."""
        self.playerRoundScore[self.roundNum] *= 2

    def addPoints(self, points):
        """Add points to the player's score for the current round.

        Args:
            points - Number of points to add. Integer. May be negative.
        Return:
            None.
        
        """
        self.playerRoundScore[self.roundNum] += points

    def grantSpinToken(self):
        """Grant one free spin token to the user."""
        self.playerTokenCount += 1

    def useSpinToken(self):
        """Use one of the player's free spin tokens."""
        self.playerTokenCount -= 1

    def bankrupt(self):
        """Set the player's score for the current round to 0."""
        self.playerRoundScore[self.roundNum] = 0

    def roundEnd(self):
        """Move onto the next round."""
        self.roundNum += 1

    def finalScore(self):
        """Get the player's final score.

        Args:
            None.
        Return:
            Sum of the player's score for each round.
        
        """
        return self.playerRoundScore[0] + self.playerRoundScore[1]