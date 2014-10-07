from TokenSet import TokenSet
from StateSet import StateSet

class GameServer():
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
        if user not in self._users:
            raise Exception('User does not exist')
        if game not in self._games:
            raise Exception('Game does not exist')
        if self._tokens.hasActiveToken(user, game):
            raise Exception('User has an existing game session')
        state = self._games[game].newGame()
        self._gameStates.setState(user, game, state)
        token = self._tokens.newToken(user, game)
        return token, state

    def play(self, user, game, move, token):
        if user not in self._users:
            raise Exception('User does not exist')
        if game not in self._games:
            raise Exception('Game does not exist')
        if not self._tokens.isValid(user, game, token):
            raise Exception('No matching game session found')
        state = self._gameStates[(user, game)]
        state = self._games[game].play(state, move)
        if state.gameOver:
            self._tokens.removeToken(user, game)
            if state.userWon:
                #self._stats.addWin(user, game)
                pass
            else:
                #self._stats.addLoss(user, game)
                pass
        return state
