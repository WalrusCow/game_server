class State():
    def __init__(self):
        self.gameOver = False
        self.userWon = False

    def toDict(self):
        return { 'gameOver' : self.gameOver, 'won' : self.userWon }

class StateSet():
    ''' Encapsulate the game states. '''
    def __init__(self):
        self._states = dict()
    def __delitem__(self, tpl): del self._states[tpl]
    def __getitem__(self, tpl): return self._states[tpl]
    def __setitem__(self, tpl, state): self._states[tpl] = state

    def removeState(self, user, game): del self._states[(user, game)]
    def getState(self, user, game): return self._states[(user, game)]
    def setState(self, user, game, state): self._states[(user, game)] = state
