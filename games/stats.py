from collections import defaultdict

class Stats():
    class Stat():
        def __init__(self):
            self.wins = 0
            self.losses = 0
        def toDict(self):
            return {'wins': self.wins, 'losses': self.losses}
    def __init__(self):
        self._stats = defaultdict(lambda: defaultdict(Stats.Stat))
    def addWin(self, user, game):
        self._stats[user][game].wins += 1
    def addLoss(self, user, game):
        self._stats[user][game].losses += 1
    def get(self, user, game):
        return self._stats[user][game]
