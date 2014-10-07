import base64
from random import randint

class TokenSet():
    class Token():
        _keyLength = 32
        def __init__(self, keyLength=_keyLength):
            def randomBytes(n):
                # Note: Not cryptographically secure
                return bytes(randint(0, 255) for _ in range(n))
            # Random base64 string, stored as `str` not `bytes`
            self.key = base64.b64encode(randomBytes(keyLength)).decode()
            #self._time = now() #TODO

        def expired():
            ''' Return True if expired. '''
            #TODO
            return False
            #return startTime - now() > cutoff

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

    def isValid(self, token, user, game):
        if not self.hasActiveToken(user, game):
            return False
        return token == self._tokens[(user, game)].key


