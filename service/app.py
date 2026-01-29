from flask import Flask, render_template, jsonify, request, make_response, g
from games.coop import GoGameCoop
import uuid

app = Flask(__name__)

# Coop local games
coopGames = {}


@app.before_request
def ensure_user_id():
    user_id = request.cookies.get('id')

    if not user_id:
        user_id = str(uuid.uuid4())
        g.new_user_id = user_id
    else:
        g.new_user_id = None

    g.user_id = user_id


@app.after_request
def set_user_cookie(response):
    if hasattr(g, 'new_user_id') and g.new_user_id:
        response.set_cookie('id', g.new_user_id, max_age=60 *
                            60*24*30, httponly=True, samesite='Lax')
    return response


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stateCoop', methods=['GET'])
def getState():
    game = coopGames.get(g.user_id)

    if game is None:
        game = GoGameCoop(9)
        coopGames[g.user_id] = game

    return jsonify(game.toDict())


@app.route('/moveCoop', methods=['POST'])
def makeMove():
    data = request.json
    game = coopGames.get(g.user_id)

    if not game:
        return jsonify({"error": "No game found"}), 404

    success, message = game.placeStone(int(data['x']), int(data['y']))
    return jsonify({
        'success': success,
        'message': message,
        'game_state': game.toDict()
    })


@app.route('/resetCoop', methods=['POST'])
def resetGame():
    game = GoGameCoop(size=9)
    coopGames[g.user_id] = game
    return jsonify(game.toDict())


if __name__ == '__main__':
    app.run(debug=True)
