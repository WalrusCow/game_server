import base64
from datetime import datetime, timedelta
from random import randint

class TokenSet():
    ''' Encapsulate the tokens. '''
    class Token():
        _keyLength = 16
        def __init__(self, keyLength=_keyLength):
            def randomBytes(n):
                # Note: Not cryptographically secure
                return bytes(randint(0, 255) for _ in range(n))
            # Random base64 string, stored as `str` not `bytes`
            self.key = base64.b64encode(randomBytes(keyLength)).decode()
            self._time = datetime.now()
            self._lifetime = timedelta(hours=2)

        def expired(self):
            ''' Return True if expired. '''
            return datetime.now() - self._time > self._lifetime

    def __init__(self):
        # Map (user, game) -> Token
        self._tokens = dict()

    def __getitem__(self, tpl):
        return self._tokens[tpl]

    def hasActiveToken(self, user, game):
        if not (user, game) in self._tokens:
            return False
        return not self._tokens[(user, game)].expired()

    def newToken(self, user, game):
        tok = self.Token()
        self._tokens[(user, game)] = tok
        return tok.key

    def removeToken(self, user, game):
        del self._tokens[(user, game)]

    def isValid(self, user, game, token):
        if not self.hasActiveToken(user, game):
            return False
        return token == self._tokens[(user, game)].key
