from flask import Flask, render_template, request, jsonify
from game import (
    shuffle_cards,
    ai_move,
    user_takes_cards,
    user_makes_a_move,
    user_beats_the_cards,
    user_moves_the_cards,
)

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/game")
def game():
    return render_template("game.html")


@app.route("/rules")
def rules():
    return render_template("rules.html")


@app.route("/victory")
def victory():
    return render_template("victory.html")


@app.route("/game/shuffle", methods=["GET"])
def shuffle():
    return jsonify(shuffle_cards())


@app.route("/game/AImove", methods=["POST"])
def computer_move():
    data = request.get_json()
    game_state = data.get("gameState")

    updated_game_state = ai_move(game_state)
    return jsonify(updated_game_state)


@app.route("/game/takeCards", methods=["POST"])
def take_cards():
    data = request.get_json()
    game_state = data.get("gameState")
    updated_game_state = user_takes_cards(game_state)
    return jsonify(updated_game_state)


@app.route("/game/makeAmove", methods=["POST"])
def make_a_move():
    data = request.get_json()
    game_state = data.get("gameState")
    selected_player_cards = data.get("selectedPlayerCards")
    status, updated_game_state = user_makes_a_move(
        game_state, selected_player_cards
    )
    return jsonify(status, updated_game_state)


@app.route("/game/beatTheCards", methods=["POST"])
def beat_the_cards():
    data = request.get_json()
    game_state = data.get("gameState")
    selected_player_cards = data.get("selectedPlayerCards")
    status, updated_game_state = user_beats_the_cards(
        game_state, selected_player_cards
    )
    return jsonify(status, updated_game_state)


@app.route("/game/moveTheCards", methods=["POST"])
def move_the_cards():
    data = request.get_json()
    game_state = data.get("gameState")
    selected_player_cards = data.get("selectedPlayerCards")
    status, updated_game_state = user_moves_the_cards(
        game_state, selected_player_cards
    )
    return jsonify(status, updated_game_state)


if __name__ == "__main__":
    app.run(debug=True)
