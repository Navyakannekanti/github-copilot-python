import sudoku_logic


def is_valid_solution(board):
    expected = set(range(1, sudoku_logic.SIZE + 1))
    rows = [set(row) for row in board]
    columns = [
        {board[row][column] for row in range(sudoku_logic.SIZE)}
        for column in range(sudoku_logic.SIZE)
    ]
    boxes = [
        {
            board[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        }
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_column in range(0, sudoku_logic.SIZE, 3)
    ]
    return all(unit == expected for unit in rows + columns + boxes)


def test_create_empty_board_has_expected_shape_and_values():
    board = sudoku_logic.create_empty_board()

    assert len(board) == sudoku_logic.SIZE
    assert all(len(row) == sudoku_logic.SIZE for row in board)
    assert all(cell == sudoku_logic.EMPTY for row in board for cell in row)


def test_deep_copy_does_not_share_nested_rows():
    original = [[1, 2], [3, 4]]

    copied = sudoku_logic.deep_copy(original)
    copied[0][0] = 9

    assert original[0][0] == 1
    assert copied[0][0] == 9


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5
    board[1][4] = 6
    board[4][1] = 7

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 2, 4, 6) is False
    assert sudoku_logic.is_safe(board, 2, 2, 5) is False
    assert sudoku_logic.is_safe(board, 2, 2, 8) is True


def test_fill_board_populates_a_valid_solution(solved_board):
    assert all(cell != sudoku_logic.EMPTY for row in solved_board for cell in row)
    assert is_valid_solution(solved_board)


def test_generate_puzzle_returns_matching_solution_and_requested_clues():
    clues = 35

    puzzle, solution = sudoku_logic.generate_puzzle(clues)

    assert len(puzzle) == sudoku_logic.SIZE
    assert len(solution) == sudoku_logic.SIZE
    assert is_valid_solution(solution)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == clues
    for row in range(sudoku_logic.SIZE):
        for column in range(sudoku_logic.SIZE):
            if puzzle[row][column] != sudoku_logic.EMPTY:
                assert puzzle[row][column] == solution[row][column]
