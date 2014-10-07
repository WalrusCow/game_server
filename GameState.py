class GameState():
    def __init__(self):
        self.gameOver = False
        self.userWon = False

    def toDict(self):
        return { 'gameOver' : self.gameOver, 'won' : self.userWon }
