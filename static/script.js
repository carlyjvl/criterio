let board = ["", "", "", "", "", "", "", "", ""];
let gameOver = false;

// Sonidos
const s_click = new Audio("https://www.soundjay.com/buttons/sounds/button-16.mp3");
const s_win   = new Audio("https://www.soundjay.com/misc/sounds/bell-ringing-05.mp3");
const s_lose  = new Audio("https://www.soundjay.com/misc/sounds/fail-buzzer-01.mp3");
const s_tie   = new Audio("https://www.soundjay.com/button/sounds/beep-07.mp3");

window.onload = () => {
    const container = document.getElementById("board");

    for (let i = 0; i < 9; i++) {
        const cell = document.createElement("div");
        cell.className = "cell";
        cell.dataset.index = i;
        cell.onclick = playerMove;
        container.appendChild(cell);
    }
};

function playerMove() {
    if (gameOver) return;

    const index = this.dataset.index;

    if (board[index] !== "") return;
    
    // 1. Obtener la dificultad seleccionada
    const difficulty = document.getElementById("dificultad").value; 

    s_click.play();
    board[index] = "X";
    this.innerText = "X";

    checkEndGame();

    fetch("/move", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ 
            board: board,
            difficulty: difficulty // <--- ENVÍA LA DIFICULTAD AL SERVIDOR
        })
    })
    .then(res => res.json())
    .then(data => {
        const aiMove = data.move;
        if (aiMove !== null && !gameOver) {
            board[aiMove] = "O";
            document.querySelectorAll(".cell")[aiMove].innerText = "O";
        }
        checkEndGame();
    });
}


function getWinnerCombo() {
    const combos = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ];

    for (let combo of combos) {
        const [a, b, c] = combo;
        if (board[a] && board[a] === board[b] && board[b] === board[c]) {
            return combo;
        }
    }
    return null;
}

function checkEndGame() {
    const combo = getWinnerCombo();

    if (combo) {
        gameOver = true;

        combo.forEach(i => {
            const cell = document.querySelectorAll(".cell")[i];
            cell.style.background = "#00ff99";
            cell.style.transform = "scale(1.2)";
        });

        const winner = board[combo[0]];

        if (winner === "X") {
            s_win.play();
            showWinner("¡Ganaste! 🎉🤩");
        } else {
            s_lose.play();
            showWinner("La IA ganó 🤖");
        }

        return;
    }

    if (!board.includes("")) {
        gameOver = true;
        s_tie.play();
        showWinner("¡Empate! 😐");
    }
}

function showWinner(text) {
    document.getElementById("winnerText").innerText = text;
    document.getElementById("winnerModal").style.display = "flex";
}

function closeWinner() {
    document.getElementById("winnerModal").style.display = "none";
    resetGame();
}

function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    gameOver = false;

    document.querySelectorAll(".cell").forEach(cell => {
        cell.innerText = "";
        cell.style.background = "rgba(255,255,255,0.15)";
        cell.style.transform = "scale(1)";
    });

    document.getElementById("winnerModal").style.display = "none";
}

// ... (Toda tu lógica de juego, minimax, resetGame, etc.)

// ------------------------------------
// 👥 FUNCIONES MODAL INTEGRANTES (NUEVO CÓDIGO A AGREGAR)
// ------------------------------------

function salir() {
    // Función que se llama al hacer clic en el botón 'Salir'.
    // Muestra el modal de integrantes.
    document.getElementById("integrantesModal").style.display = "flex";
}

function closeIntegrantes() {
    // Función que se llama para cerrar el modal de integrantes.
    document.getElementById("integrantesModal").style.display = "none";
}
// ... (Toda la lógica inicial de script.js, variables, window.onload, etc.)