
class Player(object):

    def __init__(self):

        self.playerTokenCount  = 0
        self.playerRoundScore  = [0,0]
        self.roundNum          = 0

    def doubleScore(self):
        self.playerRoundScore[self.roundNum] *= 2

    def addPoints(self, points):
        self.playerRoundScore[self.roundNum] += points

    def grantSpinToken(self):
        self.playerTokenCount += 1

    def useSpinToken(self):
        self.playerTokenCount -= 1

    def bankrupt(self):
        self.playerRoundScore[self.roundNum] = 0

    def roundEnd(self):
        self.roundNum += 1

    def finalScore(self):
        return self.playerRoundScore[0] + self.playerRoundScore[1]