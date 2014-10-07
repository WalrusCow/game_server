from games.tokenSet import TokenSet
from games.states import StateSet
from games.stats import Stats

class Server():
    def __init__(self):
        self._games = dict()
        self._users = set()
        self._tokens = TokenSet()
        self._gameStates = StateSet()
        self._stats = Stats()

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
                self._stats.addWin(user, game)
                pass
            else:
                self._stats.addLoss(user, game)
                pass
        return state

    def getStats(self, user=None, game=None):
        ''' Get stats for all users, or specified user. '''
        stats = dict()
        if user is None:
            # All stats
            for user in self._users:
                stats[user] = dict()
                for game in self._games:
                    stats[user][game] = self._stats.get(user, game).toDict()
        elif game is None:
            # Stats for one user
            if user not in self._users:
                return dict()
            stats[user] = dict()
            for game in self._games:
                stats[user][game] = self._stats.get(user, game).toDict()
        else:
            # Stats for one user and one game
            if game not in self._games or user not in self._users:
                return dict()
            stats[user] = dict()
            stats[user][game] = self._stats.get(user, game).toDict()
        return stats
