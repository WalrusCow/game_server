from TokenSet import TokenSet
from StateSet import StateSet

class GameServer():
    ''' Be the "server" for the games.
    Note: Not actually a server, more like a registry
    '''
    def __init__(self):
        self._games = dict()
        self._users = set()
        self._tokens = TokenSet()
        self._gameStates = StateSet()
        #self._stats = Stats()

    def registerUser(self, user):
        if user in self._users:
            raise Exception('User already exists')
        self._users.add(user)

    def registerGame(self, name, game):
        self._games[name] = game

    def newGame(self, user, game):
        if self._tokens.hasActiveToken(user, game):
            raise Exception('User has an existing game session')
        state = self._games[game].newGame()
        self._gameStates.setState(user, game, state)
        return self._tokens.newToken(user, game), state

    def play(self, user, game, move, token):
        if not self._tokens.isValid(user, game, token):
            raise Exception('User does not have an active game session')
        state = self._gameStates[user][game]
        state = self._games[game].play(state, move)
        if state.gameOver:
            self._tokens.removeToken(user, game)
            if resultState.userWon:
                #self._stats.addWin(user, game)
                pass
            else:
                pass
                #self._stats.addLoss(user, game)
        return resultState
