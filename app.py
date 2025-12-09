import random
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


def check_winner(board):
    
    win_combos = [
        [0,1,2], [3,4,5], [6,7,8],  # filas
        [0,3,6], [1,4,7], [2,5,8],  # columnas
        [0,4,8], [2,4,6]            # diagonales
    ]

    
    for combo in win_combos:
        a, b, c = combo
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]

    # si no quedan espacios vacíos es empate
    if "" not in board:
        return "tie"

    return None


def minimax(board, player):
    result = check_winner(board)

    if result == "O":
        return 1
    elif result == "X":
        return -1
    elif result == "tie":
        return 0

    # turno de la IA
    if player == "O":
        best_value = -999
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, "X")
                board[i] = ""
                if score > best_value:
                    best_value = score
        return best_value
    else:
        worst_value = 999
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, "O")
                board[i] = ""
                if score < worst_value:
                    worst_value = score
        return worst_value


def get_ai_move(board, difficulty):
    empty = [i for i, x in enumerate(board) if x == ""]

    if len(empty) == 0:
        return None

    if difficulty == "easy":
        error_chance = 0.55
    elif difficulty == "normal":
        error_chance = 0.30
    else:
        error_chance = 0
    if random.random() < error_chance:
        return random.choice(empty)

    best_score = -99999
    best_move = None

    for pos in empty:
        board[pos] = "O"
        score = minimax(board, "X")
        board[pos] = ""
        if score > best_score:
            best_score = score
            best_move = pos

    return best_move


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    data = request.get_json()
    

    board = data.get("board", [])

    difficulty = data.get("difficulty", "expert")

    ai_choice = get_ai_move(board, difficulty)

    return jsonify({"move": ai_choice})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
