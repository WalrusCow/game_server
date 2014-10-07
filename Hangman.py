import random

from GameState import GameState

class HangmanState(GameState):
    # Some random words
    _words = ['cousin', 'garrulous', 'maleficent', 'impairment', 'sneaker',
              'liableness', 'association', 'catechism', 'effigies', 'pork',
              'mechanization', 'noisy', 'affirmative', 'sunglasses', 'belly']
    def __init__(self):
        super().__init__()
        self.secret = random.choice(HangmanState._words)
        self.guessed = set()
        self.unguessed = set(self.secret)
        self.strikes = 5

    def toDict(self):
        d = super().toDict()
        d['guessed'] = list(self.guessed)
        d['strikes'] = self.strikes
        d['secret'] = ''.join(c if c in self.guessed else '_'
                              for c in self.secret)
        return d

class Hangman():
    ''' Hangman game class. '''
    @staticmethod
    def newGame():
        return HangmanState()

    @staticmethod
    def play(state, move):
        if state.gameOver:
            raise Exception('Game is over')
        if not isinstance(move, str) or not len(move) == 1:
            raise Exception('Invalid guess')
        if move in state.guessed:
            raise Exception('Already guessed {}'.format(move))

        state.guessed.add(move)
        if move in state.unguessed:
            state.unguessed.discard(move)
            if len(state.unguessed) == 0:
                state.gameOver = True
                state.userWon = True
        else:
            state.strikes -= 1
            if state.strikes == 0:
                state.gameOver = True
        return state
