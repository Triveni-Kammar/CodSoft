from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

def check_winner(board):
    # rows, columns and diagonals sum
    for i in range(3):
        if abs(sum(board[i, :])) == 3:
            return np.sign(sum(board[i, :]))
        if abs(sum(board[:, i])) == 3:
            return np.sign(sum(board[:, i]))
    diag1 = sum(board[i, i] for i in range(3))
    if abs(diag1) == 3:
        return np.sign(diag1)
    diag2 = sum(board[i, 2 - i] for i in range(3))
    if abs(diag2) == 3:
        return np.sign(diag2)
    if not 0 in board:
        return 0  # Draw
    return None  # Game is ongoing

def minimax(board, player):
    winner = check_winner(board)
    if winner is not None:
        return winner * player, None

    best_score = -2
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i, j] == 0:
                board[i, j] = player
                score, _ = minimax(board, -player)
                score = -score
                board[i, j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_score, best_move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    web_board = data['board']
    # Map X=1, O=-1, None=0
    board = np.array([1 if x == 'X' else -1 if x == 'O' else 0 for x in web_board]).reshape((3, 3))
    _, move = minimax(board, -1)  # AI is O(-1)
    if move:
        move_index = move[0] * 3 + move[1]
    else:
        move_index = None
    return jsonify({'move': move_index})

@app.route('/check', methods=['POST'])
def check():
    data = request.json
    web_board = data['board']
    board = np.array([1 if x == 'X' else -1 if x == 'O' else 0 for x in web_board]).reshape((3, 3))
    winner_code = check_winner(board)
    if winner_code == 1:
        return jsonify({'winner': 'You'})
    elif winner_code == -1:
        return jsonify({'winner': 'AI'})
    elif winner_code == 0:
        return jsonify({'winner': 'draw'})
    else:
        return jsonify({'winner': None})

if __name__ == '__main__':
    app.run(debug=True)
