"""Tests for Sudoku unique solution requirement."""

import pytest
from sudoku_logic import (
    generate_puzzle,
    _count_solutions,
    create_empty_board,
    fill_board,
    SIZE,
    EMPTY,
)


class TestCountSolutions:
    """Tests for the _count_solutions() helper function."""

    def test_count_solutions_single_solution(self):
        """Verify _count_solutions correctly counts single-solution puzzles."""
        puzzle, _ = generate_puzzle(clues=35)
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_count_solutions_zero_solutions_invalid_puzzle(self):
        """Verify _count_solutions returns 0 for invalid/unsolvable puzzles."""
        # Create an intentionally invalid puzzle (duplicate 1s in first row)
        board = [
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
        count = _count_solutions(board, max_count=2)
        assert count == 0

    def test_count_solutions_early_termination_deterministic(self):
        """Verify _count_solutions stops at max_count with known multi-solution puzzle.
        
        Uses a fixed, known Sudoku puzzle that has multiple solutions.
        The pattern of givens is arranged such that multiple valid completions exist.
        This is a minimal but well-known multi-solution puzzle.
        """
        # Known multi-solution puzzle: minimal clues arranged to allow multiple fills
        board = [
            [0, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        # Should return exactly 2 (early termination at max_count)
        count = _count_solutions(board, max_count=2)
        assert count == 2

    def test_count_solutions_respects_max_count(self):
        """Verify _count_solutions returns max_count when limit is reached.
        
        Uses the same known multi-solution puzzle to verify that the function
        stops as soon as max_count solutions are found, not before.
        """
        board = [
            [0, 0, 0, 0, 0, 0, 0, 1, 2],
            [0, 0, 0, 0, 0, 0, 0, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        # With max_count=2, should return exactly 2
        count = _count_solutions(board, max_count=2)
        assert count == 2

    def test_count_solutions_does_not_mutate_board(self):
        """Verify _count_solutions does not modify the input board."""
        board = [
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
        board_copy = [row[:] for row in board]
        _count_solutions(board, max_count=2)
        assert board == board_copy


class TestGeneratePuzzleUniqueSolution:
    """Tests for generate_puzzle() unique solution guarantee."""

    def test_generate_puzzle_returns_unique_solution_default(self):
        """Verify generate_puzzle() with default clues=35 has exactly one solution."""
        for _ in range(3):  # Run multiple times to verify consistency
            puzzle, solution = generate_puzzle()
            count = _count_solutions(puzzle, max_count=2)
            assert count == 1, f"Expected 1 solution, got {count}"

    def test_generate_puzzle_returns_unique_solution_hard(self):
        """Verify generate_puzzle(clues=17) returns puzzle with exactly one solution."""
        puzzle, solution = generate_puzzle(clues=17)
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_returns_unique_solution_medium(self):
        """Verify generate_puzzle(clues=30) returns puzzle with exactly one solution."""
        puzzle, solution = generate_puzzle(clues=30)
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_returns_unique_solution_easy(self):
        """Verify generate_puzzle(clues=40) returns puzzle with exactly one solution."""
        puzzle, solution = generate_puzzle(clues=40)
        count = _count_solutions(puzzle, max_count=2)
        assert count == 1

    def test_generate_puzzle_respects_exact_clue_count(self):
        """Verify returned puzzle has exactly the requested number of clues."""
        for clues in [17, 25, 30, 35, 40]:
            puzzle, _ = generate_puzzle(clues=clues)
            actual_clues = sum(1 for row in puzzle for cell in row if cell != EMPTY)
            assert actual_clues == clues, \
                f"Requested {clues} clues, got {actual_clues}"

    def test_generate_puzzle_preserves_return_format(self):
        """Verify return type is tuple[list[list[int]], list[list[int]]]."""
        puzzle, solution = generate_puzzle()
        
        # Check types
        assert isinstance(puzzle, list), "puzzle should be a list"
        assert isinstance(solution, list), "solution should be a list"
        
        # Check dimensions
        assert len(puzzle) == SIZE, f"puzzle should have {SIZE} rows"
        assert len(solution) == SIZE, f"solution should have {SIZE} rows"
        
        for row_idx, (puzzle_row, solution_row) in enumerate(zip(puzzle, solution)):
            assert len(puzzle_row) == SIZE, \
                f"puzzle row {row_idx} should have {SIZE} cols"
            assert len(solution_row) == SIZE, \
                f"solution row {row_idx} should have {SIZE} cols"

    def test_generate_puzzle_solution_is_complete(self):
        """Verify solution has all cells filled (no EMPTY/0 values)."""
        _, solution = generate_puzzle()
        for row_idx, row in enumerate(solution):
            for col_idx, cell in enumerate(row):
                assert cell != EMPTY, \
                    f"Solution has empty cell at [{row_idx}][{col_idx}]"

    def test_generate_puzzle_puzzle_contains_empty_cells(self):
        """Verify puzzle has empty cells (is not already solved)."""
        puzzle, _ = generate_puzzle(clues=35)
        empty_count = sum(1 for row in puzzle for cell in row if cell == EMPTY)
        assert empty_count > 0, "Puzzle should have empty cells"

    def test_generate_puzzle_signature_unchanged(self):
        """Verify function signature is backward compatible."""
        # Test with no arguments (default)
        puzzle1, solution1 = generate_puzzle()
        assert puzzle1 is not None and solution1 is not None
        
        # Test with explicit clues argument
        puzzle2, solution2 = generate_puzzle(clues=25)
        assert puzzle2 is not None and solution2 is not None
