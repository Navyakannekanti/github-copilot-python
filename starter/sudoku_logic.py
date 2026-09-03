"""Sudoku puzzle generation and validation logic.

This module provides functions to generate valid Sudoku puzzles and validate
solutions. It implements a backtracking algorithm to fill boards and a
randomized cell removal algorithm to create puzzle difficulty.
"""

import copy
import random

# Sudoku board constants
SIZE = 9
EMPTY = 0
BOX_SIZE = 3


def create_empty_board():
    """Create an empty 9x9 Sudoku board filled with zeros.

    Returns:
        list[list[int]]: A 9x9 board with all cells set to EMPTY (0).
    """
    return [[EMPTY for _ in range(SIZE)] for _ in range(SIZE)]


def _get_box_start(position):
    """Get the starting row and column of the 3x3 box for a given position.

    Args:
        position (int): A row or column index (0-8).

    Returns:
        int: The starting index of the box (0, 3, or 6).
    """
    return position - position % BOX_SIZE


def _is_valid_in_box(board, start_row, start_col, num):
    """Check if a number is already present in a 3x3 box.

    Args:
        board (list[list[int]]): The Sudoku board.
        start_row (int): The starting row of the 3x3 box.
        start_col (int): The starting column of the 3x3 box.
        num (int): The number to check (1-9).

    Returns:
        bool: False if num is found in the box, True otherwise.
    """
    for i in range(BOX_SIZE):
        for j in range(BOX_SIZE):
            if board[start_row + i][start_col + j] == num:
                return False
    return True


def is_safe(board, row, col, num):
    """Check if placing a number at a position is valid.

    Validates that the number is not already present in the same row, column,
    or 3x3 box.

    Args:
        board (list[list[int]]): The Sudoku board.
        row (int): The row index (0-8).
        col (int): The column index (0-8).
        num (int): The number to validate (1-9).

    Returns:
        bool: True if the placement is valid, False otherwise.
    """
    # Check row and column
    for x in range(SIZE):
        if board[row][x] == num or board[x][col] == num:
            return False

    # Check 3x3 box
    start_row = _get_box_start(row)
    start_col = _get_box_start(col)
    return _is_valid_in_box(board, start_row, start_col, num)


def fill_board(board):
    """Fill a Sudoku board using backtracking with randomized candidates.

    This function mutates the input board in place. It iterates through each
    cell and attempts to fill empty cells with valid numbers, backtracking
    if no valid candidate exists.

    Args:
        board (list[list[int]]): The Sudoku board to fill. Modified in place.

    Returns:
        bool: True if the board was successfully filled, False if no solution exists.
    """
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True


def remove_cells(board, clues):
    """Remove cells from a completed board to create a puzzle.

    This function mutates the input board in place by randomly removing
    cell values until the desired number of clues remains.

    Args:
        board (list[list[int]]): The completed Sudoku board to modify. Modified in place.
        clues (int): The target number of cells to remain filled (typically 17-40).
    """
    attempts = SIZE * SIZE - clues
    removed = set()

    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        cell = (row, col)

        if cell not in removed and board[row][col] != EMPTY:
            board[row][col] = EMPTY
            removed.add(cell)
            attempts -= 1


def generate_puzzle(clues=35):
    """Generate a random Sudoku puzzle with its solution.

    Creates a valid completed board, then removes cells to create a puzzle
    with the specified number of clues (visible numbers).

    Args:
        clues (int): The number of visible cells in the puzzle (default: 35).
            Typically ranges from 17 (hard) to 40 (easy).

    Returns:
        tuple[list[list[int]], list[list[int]]]: A tuple containing:
            - puzzle: The Sudoku puzzle with empty cells (0s).
            - solution: The complete, solved Sudoku board.
    """
    board = create_empty_board()
    fill_board(board)
    solution = copy.deepcopy(board)
    remove_cells(board, clues)
    puzzle = copy.deepcopy(board)
    return puzzle, solution
