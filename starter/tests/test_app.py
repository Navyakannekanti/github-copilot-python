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
