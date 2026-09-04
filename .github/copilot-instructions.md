# Sudoku Project Instructions

## Project Scope

This repository contains a Python Flask Sudoku application.

- Keep Sudoku business logic in `starter/sudoku_logic.py`.
- Keep HTTP routing and request/response handling in `starter/app.py`.
- Keep HTML templates in `starter/templates/`.
- Keep browser-side JavaScript and CSS in `starter/static/`.
- Keep automated tests in `starter/tests/`.

## Python Code

- Write clean, readable, maintainable Python.
- Use small, focused functions with single responsibilities.
- Use clear and descriptive names.
- Add type hints where they improve clarity and maintainability.
- Preserve existing public behavior and interfaces during refactoring unless a change is explicitly requested.
- Keep Sudoku generation, validation, and board manipulation separate from Flask routes.
- Avoid unnecessary global state and dependencies unless the existing design or assignment requires them.
- Handle errors clearly and consistently.

## Testing

- Use pytest for automated tests.
- Add focused tests for new or changed behavior.
- Prefer independent tests and reusable pytest fixtures where they improve clarity.
- Preserve characterization tests for existing behavior during refactoring.
- Never remove, skip, weaken, or rewrite tests merely to make them pass.
- Run the test suite after significant changes:
  
  `.venv\Scripts\python.exe -m pytest -q`

- Investigate test failures and correct the implementation or test expectation based on the intended behavior.

## Frontend

- Preserve the existing Flask template and static-file structure.
- Keep frontend code responsive across desktop and mobile viewports.
- Maintain accessible markup, controls, labels, focus behavior, color contrast, and user feedback where practical.
- Keep browser-side interaction logic separate from server-side Sudoku logic.
- Avoid adding frontend frameworks or dependencies unless they are necessary and explicitly justified.

## Assignment Requirements

When implementing requested application features, preserve and support the assignment requirements:

- Generate valid Sudoku puzzles with unique solutions.
- Support difficulty selection.
- Provide a timer.
- Provide solution checking and immediate input feedback.
- Provide hints with clear visual indication.
- Provide a check-puzzle workflow.
- Store and display the top ten scores with the user's name, time, hints used, and difficulty.
- Keep the application responsive and accessible.
- Show useful completion feedback, including time and hints used.

Do not implement assignment features speculatively. Implement only the features requested in the current task.

## Change Process

- Explain proposed major changes before applying them.
- Make changes incrementally in small, reviewable steps.
- Before editing, inspect the relevant source code, tests, and existing conventions.
- Make the smallest change that fully addresses the request.
- Avoid modifying unrelated functionality, formatting, or files.
- Do not change `app.py` or `sudoku_logic.py` unless the current task explicitly requires application-code changes.
- Update tests and documentation when they are directly affected by a behavior change.
