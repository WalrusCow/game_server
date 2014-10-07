import functools

from flask import Flask, jsonify, request

from Hangman import Hangman
from GameServer import GameServer

app = Flask(__name__)
gameServer = GameServer()
gameServer.registerGame('hangman', Hangman)

def hasKeys(keyList):
    ''' Decorate a route to return error if the given json does not contain
    all of the keys in `keyList`. '''
    def _decorator(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            json = request.get_json(force=True)
            if not all(k in json for k in keyList):
                return jsonify(error='Bad request')
            return func(*args, **kwargs)
        return _wrapper
    return _decorator

@app.route('/play/', methods=['GET', 'POST'])
@hasKeys(['username', 'game', 'token', 'move'])
def play():
    ''' Play a move on the game. '''
    json = request.get_json(force=True)

    try:
        state = gameServer.play(json['username'], json['game'], json['move'],
                                json['token'])
        return jsonify(**state.toDict())
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify(error=str(e))

@app.route('/new/', methods=['GET', 'POST'])
@hasKeys(['username', 'game'])
def newGame():
    json = request.get_json(force=True)

    try:
        token, gameState = gameServer.newGame(json['username'], json['game'])
        return jsonify(token=token, state=gameState.toDict())
    except Exception as e:
        return jsonify(error=str(e))

@app.route('/signup/', methods=['GET', 'POST'])
@hasKeys(['username'])
def signup():
    ''' Create a new user. '''
    json = request.get_json(force=True)

    try:
        gameServer.registerUser(json['username'])
        return jsonify(success=True)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
