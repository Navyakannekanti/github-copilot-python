from flask import Flask, render_template, jsonify, request
import sudoku_logic
import random

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

# Map difficulty levels to clue counts
DIFFICULTY_MAPPING = {
    'easy': 45,
    'medium': 35,
    'hard': 30,
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new')
def new_game():
    # Accept both 'difficulty' and 'clues' for backward compatibility
    difficulty = request.args.get('difficulty', 'medium').lower()
    clues = request.args.get('clues')
    
    # If clues is provided, use it (backward compatibility)
    if clues is not None:
        clues = int(clues)
    # Otherwise, map difficulty to clues
    elif difficulty in DIFFICULTY_MAPPING:
        clues = DIFFICULTY_MAPPING[difficulty]
    else:
        return jsonify({'error': f'Invalid difficulty: {difficulty}'}), 400
    
    puzzle, solution = sudoku_logic.generate_puzzle(clues)
    CURRENT['puzzle'] = puzzle
    CURRENT['solution'] = solution
    return jsonify({'puzzle': puzzle})

@app.route('/check', methods=['POST'])
def check_solution():
    data = request.json
    board = data.get('board')
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    incorrect = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if board[i][j] != solution[i][j]:
                incorrect.append([i, j])
    return jsonify({'incorrect': incorrect})

@app.route('/hint', methods=['POST'])
def get_hint():
    """Return a hint: a random unfilled cell with its correct value."""
    puzzle = CURRENT.get('puzzle')
    solution = CURRENT.get('solution')
    
    if puzzle is None or solution is None:
        return jsonify({'error': 'No game in progress'}), 400
    
    # Find all empty cells in the puzzle
    empty_cells = []
    for i in range(sudoku_logic.SIZE):
        for j in range(sudoku_logic.SIZE):
            if puzzle[i][j] == sudoku_logic.EMPTY:
                empty_cells.append((i, j))
    
    if not empty_cells:
        return jsonify({'error': 'No empty cells for hint'}), 400
    
    # Pick a random empty cell
    row, col = random.choice(empty_cells)
    value = solution[row][col]
    
    return jsonify({
        'row': row,
        'col': col,
        'value': value
    })

if __name__ == '__main__':
    app.run(debug=True)