
class Player(object):

    def __init__(self):

        self.playerScore       = 0
        self.playerTokenCount  = 0
        self.playerRound1Score = 0
        self.playerRound2Score = 0
        self.playerFinalScore  = 0

    def doubleScore(self):
        self.playerScore *= 2

    def addPoints(self, points):
        self.playerScore += points

    def grantSpinToken(self):
        self.playerTokenCount += 1

    def useSpinToken(self):
        self.playerTokenCount -= 1

    def bankrupt(self):
        self.playerScore = 0

    def roundEnd(self):
        self.playerRoundScore = self.playerScore
        self.playerScore = 0

    def finalScore(self):
        self.playerFinalScore = self.playerRoundScore + self.playerScore