from .states import State

class ChallengeState(State):
    def __init__(self):
        self.challenge = 'What is the airspeed velocity of an unladen swallow?'
        super().__init__()

    def toDict(self):
        d = super().toDict()
        d['challenge'] = self.challenge
        return d

class Challenge():
    ''' Challenge game class. '''
    @staticmethod
    def newGame():
        return ChallengeState()

    @staticmethod
    def play(state, response):
        if state.gameOver:
            raise Exception('Game is over')
        state.gameOver = True
        if isinstance(response, str) and response.endswith('?'):
            state.userWon = True
        elif response in [11, '11', '11m/s', '11 m/s']:
            state.userWon = True
        return state
