from flask import Flask, render_template, jsonify, request
from gameLogic.goGame import GoGame


app = Flask(__name__)

game = GoGame(size=9)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/state', methods=['GET'])
def getState():
    return jsonify(game.to_dict())


@app.route('/move', methods=['POST'])
def make_move():
    data = request.json
    x = int(data['x'])
    y = int(data['y'])

    success, message = game.placeStone(x, y)
    return jsonify({
        'success': success,
        'message': message,
        'game_state': game.to_dict()
    })


@app.route('/reset', methods=['POST'])
def reset_game():
    global game
    game = GoGame(size=9)
    return jsonify(game.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
