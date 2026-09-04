import pytest

import app
import sudoku_logic


@pytest.fixture
def client():
    app.app.config.update(TESTING=True)
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT['puzzle'] = None
    app.CURRENT['solution'] = None


@pytest.fixture
def solved_board():
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)
    return board
