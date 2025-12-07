from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Función para verificar ganador
def check_winner(board):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],  # filas
        [0,3,6], [1,4,7], [2,5,8],  # columnas
        [0,4,8], [2,4,6]            # diagonales
    ]

    for a,b,c in win_conditions:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "tie"

    return None

# Minimax
def minimax(board, player):
    winner = check_winner(board)
    if winner == "O": return 1
    if winner == "X": return -1
    if winner == "tie": return 0

    if player == "O":
        best = -999
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, "X")
                board[i] = ""
                best = max(best, score)
        return best
    else:
        best = 999
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, "O")
                board[i] = ""
                best = min(best, score)
        return best

def get_best_move(board):
    best_score = -999
    move = None
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            score = minimax(board, "X")
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
    return move

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    best_move = get_best_move(board)
    return jsonify({"move": best_move})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


