"""Tests for Sudoku unique solution requirement."""

import pytest
from sudoku_logic import (
    generate_puzzle,
    _count_solutions,
    SIZE,
    EMPTY,
)


class TestCountSolutions:
    """Tests for the _count_solutions() helper function."""

    def test_count_solutions_single_solution_deterministic(self):
        """Verify _count_solutions correctly counts single-solution puzzles.
        
        Uses a deterministic single-solution Sudoku board.
        Completes in < 1 second.
        """
        unique_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        count = _count_solutions(unique_board, max_count=2)
        assert count == 1

    def test_count_solutions_zero_solutions_invalid_board(self):
        """Verify _count_solutions returns 0 for boards with conflicting clues.
        
        Uses a board with duplicate 1s in row 0, which violates Sudoku rules.
        With the enhanced _count_solutions validation, this returns 0 immediately
        without backtracking. Completes in < 0.01 seconds.
        """
        # Invalid: duplicate 1 in row 0
        invalid_board = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        count = _count_solutions(invalid_board, max_count=2)
        assert count == 0

    def test_count_solutions_multiple_solutions_deterministic(self):
        """Verify _count_solutions detects multiple solutions and stops at max_count.
        
        Uses a verified multi-solution board with exactly 2 solutions.
        This board is derived from a valid complete Sudoku with specific clues
        removed to create exactly 2 valid completions.
        Early termination at max_count=2 ensures fast completion (< 0.5s).
        """
        # Verified multi-solution board: exactly 2 solutions
        multi_solution_board = [
            [5, 3, 4, 0, 0, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 0, 0, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
        count = _count_solutions(multi_solution_board, max_count=2)
        assert count == 2

    def test_count_solutions_respects_max_count_parameter(self):
        """Verify _count_solutions stops immediately when max_count is reached.
        
        Uses the same verified multi-solution board to confirm that the max_count
        parameter causes early termination at exactly that count.
        """
        multi_solution_board = [
            [5, 3, 4, 0, 0, 8, 9, 1, 2],
            [6, 7, 2, 1, 9, 5, 3, 4, 8],
            [1, 9, 8, 3, 4, 2, 5, 6, 7],
            [8, 5, 9, 0, 0, 1, 4, 2, 3],
            [4, 2, 6, 8, 5, 3, 7, 9, 1],
            [7, 1, 3, 9, 2, 4, 8, 5, 6],
            [9, 6, 1, 5, 3, 7, 2, 8, 4],
            [2, 8, 7, 4, 1, 9, 6, 3, 5],
            [3, 4, 5, 2, 8, 6, 1, 7, 9],
        ]
        count = _count_solutions(multi_solution_board, max_count=2)
        assert count == 2, "Should stop at max_count=2"

    def test_count_solutions_does_not_mutate_input_board(self):
        """Verify _count_solutions does not modify the input board.
        
        Tests with an invalid board (quick return) to verify immutability.
        """
        original_board = [
            [1, 1, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        board_copy = [row[:] for row in original_board]
        _count_solutions(original_board, max_count=2)
        assert original_board == board_copy, "Input board should not be mutated"


class TestGeneratePuzzleUniqueSolution:
    """Tests for generate_puzzle() unique solution guarantee."""

    def test_generate_puzzle_returns_unique_solution_default(self):
        """Verify generate_puzzle() with default clues=35 has exactly one solution.
        
        Runs 3 times to verify consistency across multiple generations.
        Each puzzle is verified to have exactly 1 solution.
        """
        for _ in range(3):
            puzzle, solution = generate_puzzle()
            count = _count_solutions(puzzle, max_count=2)
            assert count == 1, f"Expected 1 solution, got {count}"

    def test_generate_puzzle_returns_unique_solution_easy(self):
        """Verify generate_puzzle(clues=45) returns puzzle with exactly one solution.
        
        Tests easy difficulty (45 clues).
        Verifies: exact clue count, 9x9 dimensions, puzzle matches solution,
        solution is complete, and unique solution.
        """
        puzzle, solution = generate_puzzle(clues=45)
        
        # Verify exact clue count
        actual_clues = sum(1 for row in puzzle for cell in row if cell != EMPTY)
        assert actual_clues == 45
        
        # Verify puzzle dimensions
        assert len(puzzle) == SIZE
        assert all(len(row) == SIZE for row in puzzle)
        
        # Verify solution dimensions
        assert len(solution) == SIZE
        assert all(len(row) == SIZE for row in solution)
        
        # Verify all non-empty puzzle cells match solution
        for row in range(SIZE):
            for col in range(SIZE):
                if puzzle[row][col] != EMPTY:
                    assert puzzle[row][col] == solution[row][col]
        
        # Verify solution is complete (no empty cells)
        assert all(cell != EMPTY for row in solution for cell in row)
        
        # Verify unique solution
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_returns_unique_solution_medium(self):
        """Verify generate_puzzle(clues=35) returns puzzle with exactly one solution.
        
        Tests medium difficulty (35 clues).
        Verifies: exact clue count, 9x9 dimensions, puzzle matches solution,
        solution is complete, and unique solution.
        """
        puzzle, solution = generate_puzzle(clues=35)
        
        # Verify exact clue count
        actual_clues = sum(1 for row in puzzle for cell in row if cell != EMPTY)
        assert actual_clues == 35
        
        # Verify puzzle dimensions
        assert len(puzzle) == SIZE
        assert all(len(row) == SIZE for row in puzzle)
        
        # Verify solution dimensions
        assert len(solution) == SIZE
        assert all(len(row) == SIZE for row in solution)
        
        # Verify all non-empty puzzle cells match solution
        for row in range(SIZE):
            for col in range(SIZE):
                if puzzle[row][col] != EMPTY:
                    assert puzzle[row][col] == solution[row][col]
        
        # Verify solution is complete (no empty cells)
        assert all(cell != EMPTY for row in solution for cell in row)
        
        # Verify unique solution
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_returns_unique_solution_hard(self):
        """Verify generate_puzzle(clues=30) returns puzzle with exactly one solution.
        
        Tests hard difficulty (30 clues).
        Verifies: exact clue count, 9x9 dimensions, puzzle matches solution,
        solution is complete, and unique solution.
        Completes in 1-2 seconds per generation.
        """
        puzzle, solution = generate_puzzle(clues=30)
        
        # Verify exact clue count
        actual_clues = sum(1 for row in puzzle for cell in row if cell != EMPTY)
        assert actual_clues == 30
        
        # Verify puzzle dimensions
        assert len(puzzle) == SIZE
        assert all(len(row) == SIZE for row in puzzle)
        
        # Verify solution dimensions
        assert len(solution) == SIZE
        assert all(len(row) == SIZE for row in solution)
        
        # Verify all non-empty puzzle cells match solution
        for row in range(SIZE):
            for col in range(SIZE):
                if puzzle[row][col] != EMPTY:
                    assert puzzle[row][col] == solution[row][col]
        
        # Verify solution is complete (no empty cells)
        assert all(cell != EMPTY for row in solution for cell in row)
        
        # Verify unique solution
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_respects_exact_clue_count(self):
        """Verify returned puzzle has exactly the requested number of clues.
        
        Tests the actual application difficulty levels (45, 35, 30)
        to ensure the function never silently changes the clue count.
        """
        for clues in [45, 35, 30]:
            puzzle, _ = generate_puzzle(clues=clues)
            actual_clues = sum(1 for row in puzzle for cell in row if cell != EMPTY)
            assert actual_clues == clues, (
                f"Requested {clues} clues, got {actual_clues}"
            )

    def test_generate_puzzle_preserves_return_format(self):
        """Verify return type is tuple[list[list[int]], list[list[int]]].
        
        Validates structure and dimensions of returned puzzle and solution.
        """
        puzzle, solution = generate_puzzle()
        
        # Check types
        assert isinstance(puzzle, list), "puzzle should be a list"
        assert isinstance(solution, list), "solution should be a list"
        
        # Check dimensions
        assert len(puzzle) == SIZE, f"puzzle should have {SIZE} rows"
        assert len(solution) == SIZE, f"solution should have {SIZE} rows"
        
        for row_idx, (puzzle_row, solution_row) in enumerate(zip(puzzle, solution)):
            assert len(puzzle_row) == SIZE, (
                f"puzzle row {row_idx} should have {SIZE} cols"
            )
            assert len(solution_row) == SIZE, (
                f"solution row {row_idx} should have {SIZE} cols"
            )

    def test_generate_puzzle_solution_is_complete(self):
        """Verify solution has all cells filled (no EMPTY/0 values)."""
        _, solution = generate_puzzle()
        for row_idx, row in enumerate(solution):
            for col_idx, cell in enumerate(row):
                assert cell != EMPTY, (
                    f"Solution has empty cell at [{row_idx}][{col_idx}]"
                )

    def test_generate_puzzle_puzzle_contains_empty_cells(self):
        """Verify puzzle has empty cells (is not already solved)."""
        puzzle, _ = generate_puzzle(clues=35)
        empty_count = sum(1 for row in puzzle for cell in row if cell == EMPTY)
        assert empty_count > 0, "Puzzle should have empty cells"

    def test_generate_puzzle_signature_unchanged(self):
        """Verify function signature is backward compatible.
        
        Tests both default and explicit clue arguments.
        """
        # Test with no arguments (default)
        puzzle1, solution1 = generate_puzzle()
        assert puzzle1 is not None and solution1 is not None
        
        # Test with explicit clues argument
        puzzle2, solution2 = generate_puzzle(clues=25)
        assert puzzle2 is not None and solution2 is not None
