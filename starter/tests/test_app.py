import app


def test_index_renders_game_page(client):
    response = client.get('/')

    assert response.status_code == 200
    assert b'Sudoku Game' in response.data


def test_new_game_returns_puzzle_and_stores_solution(client, monkeypatch):
    puzzle = [[1 for _ in range(9)] for _ in range(9)]
    solution = [[2 for _ in range(9)] for _ in range(9)]

    def fake_generate_puzzle(clues):
        assert clues == 40
        return puzzle, solution

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new?clues=40')

    assert response.status_code == 200
    assert response.get_json() == {'puzzle': puzzle}
    assert app.CURRENT == {'puzzle': puzzle, 'solution': solution}


def test_new_game_uses_default_clue_count(client, monkeypatch):
    calls = []

    def fake_generate_puzzle(clues):
        calls.append(clues)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]

    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)

    response = client.get('/new')

    assert response.status_code == 200
    assert calls == [35]


def test_check_without_game_returns_error(client):
    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_correct_solution_returns_no_incorrect_cells(client):
    solution = [[row * 9 + column + 1 for column in range(9)] for row in range(9)]
    app.CURRENT['solution'] = solution

    response = client.post('/check', json={'board': solution})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': []}


def test_check_reports_incorrect_cell_coordinates(client):
    solution = [[1] * 9 for _ in range(9)]
    board = [row[:] for row in solution]
    board[2][4] = 0
    app.CURRENT['solution'] = solution

    response = client.post('/check', json={'board': board})

    assert response.status_code == 200
    assert response.get_json() == {'incorrect': [[2, 4]]}


def test_new_game_easy_difficulty(client, monkeypatch):
    calls = []
    
    def fake_generate_puzzle(clues):
        calls.append(clues)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]
    
    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)
    
    response = client.get('/new?difficulty=easy')
    
    assert response.status_code == 200
    assert calls == [45]


def test_new_game_medium_difficulty(client, monkeypatch):
    calls = []
    
    def fake_generate_puzzle(clues):
        calls.append(clues)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]
    
    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)
    
    response = client.get('/new?difficulty=medium')
    
    assert response.status_code == 200
    assert calls == [35]


def test_new_game_hard_difficulty(client, monkeypatch):
    calls = []
    
    def fake_generate_puzzle(clues):
        calls.append(clues)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]
    
    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)
    
    response = client.get('/new?difficulty=hard')
    
    assert response.status_code == 200
    assert calls == [30]


def test_new_game_invalid_difficulty(client):
    response = client.get('/new?difficulty=invalid')
    
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data
    assert 'Invalid difficulty' in data['error']


def test_new_game_clues_parameter_takes_precedence(client, monkeypatch):
    calls = []
    
    def fake_generate_puzzle(clues):
        calls.append(clues)
        return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]
    
    monkeypatch.setattr(app.sudoku_logic, 'generate_puzzle', fake_generate_puzzle)
    
    response = client.get('/new?difficulty=easy&clues=40')
    
    assert response.status_code == 200
    assert calls == [40]


def test_index_includes_difficulty_selector(client):
    """Verify difficulty selector is present in the game page."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'difficulty-selector' in response.data
    assert b'Easy (45)' in response.data
    assert b'Medium (35)' in response.data
    assert b'Hard (30)' in response.data


def test_hint_endpoint_returns_empty_cell(client):
    """Verify /hint returns a random empty cell with correct value."""
    puzzle = [[1, 2, 3, 4, 5, 6, 7, 8, 0]] + [[0] * 9 for _ in range(8)]
    solution = [[1, 2, 3, 4, 5, 6, 7, 8, 9]] + [[i] * 9 for i in range(1, 9)]
    app.CURRENT['puzzle'] = puzzle
    app.CURRENT['solution'] = solution
    
    response = client.post('/hint')
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'row' in data
    assert 'col' in data
    assert 'value' in data
    assert 0 <= data['row'] < 9
    assert 0 <= data['col'] < 9
    assert 1 <= data['value'] <= 9
    # Verify the hint comes from an originally empty cell
    assert puzzle[data['row']][data['col']] == 0


def test_hint_without_game_returns_error(client):
    """Verify /hint returns error when no game in progress."""
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    
    response = client.post('/hint')
    
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert 'No game in progress' in response.get_json()['error']


def test_hint_no_empty_cells_returns_error(client):
    """Verify /hint returns error when puzzle is completely filled."""
    puzzle = [[i] * 9 for i in range(1, 10)]
    solution = [[i] * 9 for i in range(1, 10)]
    app.CURRENT['puzzle'] = puzzle
    app.CURRENT['solution'] = solution
    
    response = client.post('/hint')
    
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert 'No empty cells for hint' in response.get_json()['error']


def test_hint_returns_correct_value(client):
    """Verify /hint returns value that matches the solution."""
    puzzle = [[0] * 9 for _ in range(9)]
    solution = [[i + j for j in range(9)] for i in range(1, 10)]
    app.CURRENT['puzzle'] = puzzle
    app.CURRENT['solution'] = solution
    
    response = client.post('/hint')
    
    assert response.status_code == 200
    data = response.get_json()
    # Verify the returned value matches the solution
    assert data['value'] == solution[data['row']][data['col']]


def test_index_includes_hint_button(client):
    """Verify hint button is present in the game page."""
    response = client.get('/')
    
    assert response.status_code == 200
    assert b'id="hint"' in response.data
    assert b'Hints:' in response.data
