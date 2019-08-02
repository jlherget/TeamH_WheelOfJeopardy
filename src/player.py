
class Player(object):

    def __init__(self, playerScore, playerTokenCount, playerRoundScore, playerFinalScore):

        self.playerScore = playerScore
        self.playerTokenCount = playerTokenCount
        self.playerRoundScore = playerRoundScore
        self.playerFinalScore = playerFinalScore

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