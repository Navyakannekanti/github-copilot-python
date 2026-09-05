const SIZE = 9;

let puzzle = [];
let currentDifficulty = 'medium';

let hintCount = 0;

let timerSeconds = 0;
let timerInterval = null;

const DIFFICULTY_MAPPING = {
  easy: 45,
  medium: 35,
  hard: 30
};

const SCORE_STORAGE_KEY = 'sudokuTopScores';
const DARK_MODE_KEY = 'sudokuDarkMode';


function formatTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;

  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}


function updateTimerDisplay() {
  const timer = document.getElementById('timer');

  if (timer) {
    timer.innerText = `Time: ${formatTime(timerSeconds)}`;
  }
}


function startTimer() {
  stopTimer();

  timerSeconds = 0;
  updateTimerDisplay();

  timerInterval = setInterval(() => {
    timerSeconds += 1;
    updateTimerDisplay();
  }, 1000);
}


function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}


function resetHintCount() {
  hintCount = 0;
  updateHintDisplay();
}


function updateHintDisplay() {
  const hintCountElement = document.getElementById('hint-count');

  if (hintCountElement) {
    hintCountElement.innerText = `Hints: ${hintCount}`;
  }
}


function getScores() {
  try {
    const storedScores = localStorage.getItem(SCORE_STORAGE_KEY);

    if (!storedScores) {
      return [];
    }

    const scores = JSON.parse(storedScores);

    return Array.isArray(scores) ? scores : [];
  } catch (error) {
    console.error('Unable to load scoreboard:', error);
    return [];
  }
}


function saveScores(scores) {
  try {
    localStorage.setItem(
      SCORE_STORAGE_KEY,
      JSON.stringify(scores)
    );
  } catch (error) {
    console.error('Unable to save scoreboard:', error);
  }
}


function addScore(name) {
  const scores = getScores();

  scores.push({
    name: name.trim(),
    time: timerSeconds,
    difficulty: currentDifficulty,
    hints: hintCount
  });

  scores.sort((a, b) => a.time - b.time);

  const topScores = scores.slice(0, 10);

  saveScores(topScores);
  renderScoreboard();
}


function escapeHtml(value) {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}


function renderScoreboard() {
  const scoreboardBody = document.getElementById('scoreboard-body');

  if (!scoreboardBody) {
    return;
  }

  const scores = getScores();

  scoreboardBody.innerHTML = '';

  scores.forEach((score, index) => {
    const row = document.createElement('tr');

    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${escapeHtml(score.name)}</td>
      <td>${formatTime(score.time)}</td>
      <td>${escapeHtml(score.difficulty)}</td>
      <td>${score.hints}</td>
    `;

    scoreboardBody.appendChild(row);
  });
}


function getConflictingCells(row, col, value) {
  const conflicts = new Set();

  if (!value) {
    return conflicts;
  }

  const inputs = document.querySelectorAll('#sudoku-board .cell');

  inputs.forEach((input) => {
    const inputRow = Number(input.dataset.row);
    const inputCol = Number(input.dataset.col);

    if (inputRow === row && inputCol === col) {
      return;
    }

    if (
      input.value === value &&
      (
        inputRow === row ||
        inputCol === col ||
        (
          Math.floor(inputRow / 3) === Math.floor(row / 3) &&
          Math.floor(inputCol / 3) === Math.floor(col / 3)
        )
      )
    ) {
      conflicts.add(`${inputRow}-${inputCol}`);
    }
  });

  return conflicts;
}


function getCurrentBoard() {
  const board = Array.from(
    { length: SIZE },
    () => Array(SIZE).fill(0)
  );

  const inputs = document.querySelectorAll('#sudoku-board .cell');

  inputs.forEach((input) => {
    const row = Number(input.dataset.row);
    const col = Number(input.dataset.col);

    const value = Number(input.value);

    board[row][col] = value || 0;
  });

  return board;
}


function clearConflictHighlighting() {
  const inputs = document.querySelectorAll('#sudoku-board .cell');

  inputs.forEach((input) => {
    input.classList.remove('conflict');
  });
}


function applyConflictHighlighting(input) {
  clearConflictHighlighting();

  const value = input.value.trim();

  if (!value) {
    return;
  }

  const row = Number(input.dataset.row);
  const col = Number(input.dataset.col);

  const conflicts = getConflictingCells(row, col, value);

  if (conflicts.size === 0) {
    return;
  }

  input.classList.add('conflict');

  conflicts.forEach((position) => {
    const [conflictRow, conflictCol] = position
      .split('-')
      .map(Number);

    const conflictInput = document.querySelector(
      `#sudoku-board .cell[data-row="${conflictRow}"][data-col="${conflictCol}"]`
    );

    if (conflictInput) {
      conflictInput.classList.add('conflict');
    }
  });
}


function createBoardElement() {
  const boardElement = document.createElement('div');

  boardElement.id = 'sudoku-board';

  return boardElement;
}


function renderPuzzle(puzzleBoard) {
  const boardContainer = document.getElementById('sudoku-board');

  if (!boardContainer) {
    return;
  }

  boardContainer.innerHTML = '';

  for (let row = 0; row < SIZE; row += 1) {
    for (let col = 0; col < SIZE; col += 1) {
      const cell = document.createElement('input');

      cell.type = 'text';
      cell.inputMode = 'numeric';
      cell.maxLength = 1;

      cell.classList.add('cell');

      cell.dataset.row = row;
      cell.dataset.col = col;

      /*
       * Alternate the background color of the 3x3 Sudoku boxes.
       * This creates a checkerboard pattern across the nine boxes.
       */
      const boxRow = Math.floor(row / 3);
      const boxCol = Math.floor(col / 3);
      const isShaded = (boxRow + boxCol) % 2 === 0;

      cell.classList.add(
        isShaded ? 'box-shade' : 'box-plain'
      );

      const value = puzzleBoard[row][col];

      if (value !== 0) {
        cell.value = value;
        cell.disabled = true;
        cell.classList.add('prefilled');
      }

      cell.addEventListener('input', () => {
        cell.value = cell.value.replace(/[^1-9]/g, '');

        cell.classList.remove('incorrect');

        applyConflictHighlighting(cell);
      });

      cell.addEventListener('focus', () => {
        applyConflictHighlighting(cell);
      });

      boardContainer.appendChild(cell);
    }
  }
}


function setDifficulty(difficulty) {
  if (!DIFFICULTY_MAPPING[difficulty]) {
    return;
  }

  currentDifficulty = difficulty;

  const buttons = document.querySelectorAll(
    '.difficulty-selector button'
  );

  buttons.forEach((button) => {
    button.removeAttribute('data-selected');
  });

  const selectedButton = document.querySelector(
    `.difficulty-selector button[data-difficulty="${difficulty}"]`
  );

  if (selectedButton) {
    selectedButton.setAttribute('data-selected', 'true');
  }
}


async function requestHint() {
  const message = document.getElementById('message');

  try {
    const response = await fetch('/hint', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        board: getCurrentBoard()
      })
    });

    const data = await response.json();

    if (!response.ok) {
      message.innerText = data.error || 'Unable to provide a hint.';
      message.style.color = '#d32f2f';
      return;
    }

    const input = document.querySelector(
      `#sudoku-board .cell[data-row="${data.row}"][data-col="${data.col}"]`
    );

    if (!input) {
      return;
    }

    input.value = data.value;

    /*
     * Hinted cells are locked so the user cannot modify
     * the correct answer supplied by the hint system.
     */
    input.disabled = true;
    input.classList.add('hinted');

    hintCount += 1;
    updateHintDisplay();

    clearConflictHighlighting();

    message.innerText = 'Hint added.';
    message.style.color = '#388e3c';
  } catch (error) {
    console.error('Hint request failed:', error);

    message.innerText = 'Unable to provide a hint.';
    message.style.color = '#d32f2f';
  }
}


async function newGame() {
  const message = document.getElementById('message');

  try {
    const response = await fetch(
      `/new?difficulty=${encodeURIComponent(currentDifficulty)}`
    );

    if (!response.ok) {
      throw new Error('Unable to start a new game.');
    }

    const data = await response.json();

    puzzle = data.puzzle;

    renderPuzzle(puzzle);

    clearConflictHighlighting();

    resetHintCount();

    if (message) {
      message.innerText = '';
      message.style.color = '';
    }

    startTimer();
  } catch (error) {
    console.error('New game request failed:', error);

    if (message) {
      message.innerText = 'Unable to start a new game.';
      message.style.color = '#d32f2f';
    }
  }
}


async function checkSolution() {
  const message = document.getElementById('message');
  const board = getCurrentBoard();

  const inputs = document.querySelectorAll(
    '#sudoku-board .cell'
  );

  inputs.forEach((input) => {
    input.classList.remove('incorrect');
  });

  try {
    const response = await fetch('/check', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        board
      })
    });

    const data = await response.json();

    if (!response.ok) {
      message.innerText = data.error || 'Unable to check the solution.';
      message.style.color = '#d32f2f';
      return;
    }

    const incorrect = new Set();

    if (Array.isArray(data.incorrect)) {
      data.incorrect.forEach((position) => {
        incorrect.add(`${position[0]}-${position[1]}`);
      });
    }

    incorrect.forEach((position) => {
      const [row, col] = position
        .split('-')
        .map(Number);

      const input = document.querySelector(
        `#sudoku-board .cell[data-row="${row}"][data-col="${col}"]`
      );

      if (input) {
        input.classList.add('incorrect');
      }
    });

    if (incorrect.size === 0) {
      stopTimer();

      message.style.color = '#388e3c';

      message.innerText =
        `Congratulations! You solved it in ${formatTime(timerSeconds)} ` +
        `with ${hintCount} hint${hintCount === 1 ? '' : 's'}.`;

      const playerName = window.prompt(
        'Congratulations! Enter your name for the Top 10 scoreboard:'
      );

      if (playerName && playerName.trim()) {
        addScore(playerName);
      }
    } else {
      message.style.color = '#d32f2f';
      message.innerText = 'Some cells are incorrect.';
    }
  } catch (error) {
    console.error('Solution check failed:', error);

    message.innerText = 'Unable to check the solution.';
    message.style.color = '#d32f2f';
  }
}


function applyDarkMode(enabled) {
  document.body.classList.toggle('dark-mode', enabled);

  const toggleButton = document.getElementById(
    'dark-mode-toggle'
  );

  if (toggleButton) {
    toggleButton.innerText = enabled
      ? '☀️ Light Mode'
      : '🌙 Dark Mode';
  }
}


function initializeDarkMode() {
  const storedValue = localStorage.getItem(DARK_MODE_KEY);

  applyDarkMode(storedValue === 'true');
}


function toggleDarkMode() {
  const enabled = !document.body.classList.contains(
    'dark-mode'
  );

  applyDarkMode(enabled);

  localStorage.setItem(
    DARK_MODE_KEY,
    String(enabled)
  );
}


window.addEventListener('load', () => {
  initializeDarkMode();

  const difficultyButtons = document.querySelectorAll(
    '.difficulty-selector button'
  );

  difficultyButtons.forEach((button) => {
    button.addEventListener('click', () => {
      const difficulty = button.dataset.difficulty;

      setDifficulty(difficulty);
      newGame();
    });
  });

  const newGameButton = document.getElementById('new-game');

  if (newGameButton) {
    newGameButton.addEventListener('click', newGame);
  }

  const hintButton = document.getElementById('hint');

  if (hintButton) {
    hintButton.addEventListener('click', requestHint);
  }

  const checkButton = document.getElementById(
    'check-solution'
  );

  if (checkButton) {
    checkButton.addEventListener('click', checkSolution);
  }

  const darkModeButton = document.getElementById(
    'dark-mode-toggle'
  );

  if (darkModeButton) {
    darkModeButton.addEventListener(
      'click',
      toggleDarkMode
    );
  }

  renderScoreboard();

  newGame();
});