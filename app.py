import random # <--- ¡Asegúrate de que esto esté al inicio del archivo!
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Función para verificar ganador (NO CAMBIA)
def check_winner(board):
    win_conditions = [
        [0,1,2], [3,4,5], [6,7,8],   # filas
        [0,3,6], [1,4,7], [2,5,8],   # columnas
        [0,4,8], [2,4,6]             # diagonales
    ]

    for a,b,c in win_conditions:
        if board[a] == board[b] == board[c] != "":
            return board[a]

    if "" not in board:
        return "tie"

    return None

# Minimax (NO CAMBIA)
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


# --- NUEVA FUNCIÓN CON DIFICULTAD ---
def get_ai_move(board, difficulty):
    """
    Decide el movimiento de la IA basado en el nivel de dificultad.
    """
    empty_cells = [i for i, x in enumerate(board) if x == ""]

    if not empty_cells:
        return None 

    # --- Nivel FÁCIL: 60% de probabilidad de movimiento aleatorio
    if difficulty == "easy" and random.random() < 0.6:
        return random.choice(empty_cells)

    # --- Nivel NORMAL: 30% de probabilidad de movimiento aleatorio
    elif difficulty == "normal" and random.random() < 0.3:
        return random.choice(empty_cells)

    # --- Nivel EXPERTO (o si fallan los checks aleatorios): Usa Minimax
    else:
        best_score = -999
        move = None
        for i in empty_cells:
            board[i] = "O"
            score = minimax(board, "X")
            board[i] = ""
            if score > best_score:
                best_score = score
                move = i
        return move
# -----------------------------------


@app.route("/")
def index():
    return render_template("index.html")

# --- RUTA /move ACTUALIZADA ---
@app.route("/move", methods=["POST"])
def move():
    data = request.json
    board = data["board"]
    # Obtiene la dificultad enviada por JS, si no existe usa 'expert'
    difficulty = data.get("difficulty", "expert") 
    
    best_move = get_ai_move(board, difficulty)
    
    return jsonify({"move": best_move})
# ------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)