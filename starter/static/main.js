// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
let puzzle = [];
let currentDifficulty = 'medium';
let hintCount = 0;

let timerSeconds = 0;
let timerInterval = null;

const SCOREBOARD_KEY = 'sudokuTopScores';

function getScores() {
  try {
    const scores = JSON.parse(localStorage.getItem(SCOREBOARD_KEY));
    return Array.isArray(scores) ? scores : [];
  } catch (error) {
    return [];
  }
}

function saveScores(scores) {
  localStorage.setItem(SCOREBOARD_KEY, JSON.stringify(scores));
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
  saveScores(scores.slice(0, 10));
  renderScoreboard();
}

function renderScoreboard() {
  const tbody = document.getElementById('scoreboard-body');
  const scores = getScores();

  tbody.innerHTML = '';

  scores.forEach((score, index) => {
    const row = document.createElement('tr');

    row.innerHTML = `
      <td>${index + 1}</td>
      <td>${escapeHtml(score.name)}</td>
      <td>${formatTime(score.time)}</td>
      <td>${score.difficulty.charAt(0).toUpperCase() + score.difficulty.slice(1)}</td>
      <td>${score.hints}</td>
    `;

    tbody.appendChild(row);
  });
}

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;

  return `${String(minutes).padStart(2, '0')}:${String(remainingSeconds).padStart(2, '0')}`;
}

function updateTimerDisplay() {
  document.getElementById('timer').innerText = `Time: ${formatTime(timerSeconds)}`;
}

function startTimer() {
  stopTimer();
  timerSeconds = 0;
  updateTimerDisplay();

  timerInterval = setInterval(() => {
    timerSeconds++;
    updateTimerDisplay();
  }, 1000);
}

function stopTimer() {
  if (timerInterval !== null) {
    clearInterval(timerInterval);
    timerInterval = null;
  }
}

function getConflictingCells(board, row, col, value) {
  // Returns array of [row, col] that have same value in same row, column, or 3x3 box
  if (!value || value < 1 || value > 9) {
    return [];
  }
  
  const conflicts = new Set();
  
  // Check row
  for (let j = 0; j < SIZE; j++) {
    if (j !== col && board[row][j] === value) {
      conflicts.add(`${row},${j}`);
    }
  }
  
  // Check column
  for (let i = 0; i < SIZE; i++) {
    if (i !== row && board[i][col] === value) {
      conflicts.add(`${i},${col}`);
    }
  }
  
  // Check 3x3 box
  const boxRow = Math.floor(row / 3) * 3;
  const boxCol = Math.floor(col / 3) * 3;
  for (let i = boxRow; i < boxRow + 3; i++) {
    for (let j = boxCol; j < boxCol + 3; j++) {
      if ((i !== row || j !== col) && board[i][j] === value) {
        conflicts.add(`${i},${j}`);
      }
    }
  }
  
  return Array.from(conflicts).map(s => s.split(',').map(Number));
}

function getCurrentBoard() {
  // Build current board state from inputs
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  return board;
}

function clearConflictHighlighting() {
  // Remove .conflict class from all cells
  const boardDiv = document.getElementById('sudoku-board');
  const cells = boardDiv.getElementsByClassName('sudoku-cell');
  for (let cell of cells) {
    cell.classList.remove('conflict');
  }
}

function applyConflictHighlighting(row, col, conflicts) {
  // Apply .conflict class to the current cell and conflicting cells
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  
  // Highlight current cell if it has conflicts
  if (conflicts.length > 0) {
    const idx = row * SIZE + col;
    inputs[idx].classList.add('conflict');
    
    // Highlight conflicting cells
    for (const [confRow, confCol] of conflicts) {
      const confIdx = confRow * SIZE + confCol;
      inputs[confIdx].classList.add('conflict');
    }
  }
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
      input.className = 'sudoku-cell';
      input.dataset.row = i;
      input.dataset.col = j;
      input.addEventListener('input', (e) => {
        const val = e.target.value.replace(/[^1-9]/g, '');
        e.target.value = val;
        
        // Real-time conflict detection
        const row = parseInt(e.target.dataset.row);
        const col = parseInt(e.target.dataset.col);
        const currentBoard = getCurrentBoard();
        const value = val ? parseInt(val, 10) : 0;
        
        // Clear previous highlighting
        clearConflictHighlighting();
        
        // Check for conflicts and highlight
        if (val) {
          const conflicts = getConflictingCells(currentBoard, row, col, value);
          applyConflictHighlighting(row, col, conflicts);
        }
      });
      rowDiv.appendChild(input);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        inp.className += ' prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
      }
    }
  }
}

function setDifficulty(difficulty) {
  currentDifficulty = difficulty;
  
  // Update visual selection state
  const buttons = document.querySelectorAll('.difficulty-btn');
  buttons.forEach(btn => {
    btn.classList.remove('selected');
    if (btn.dataset.difficulty === difficulty) {
      btn.classList.add('selected');
    }
  });
  
  // Load new puzzle with selected difficulty
  newGame();
}

function resetHintCount() {
  hintCount = 0;
  updateHintDisplay();
}

function updateHintDisplay() {
  document.getElementById('hint-count').innerText = `Hints: ${hintCount}`;
}

async function requestHint() {
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'}
  });
  
  if (!res.ok) {
    const data = await res.json();
    document.getElementById('message').innerText = data.error || 'Error getting hint';
    return;
  }
  
  const data = await res.json();
  const { row, col, value } = data;
  
  // Fill the cell with the hint
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const idx = row * SIZE + col;
  
  if (inputs[idx].value === '') {
    inputs[idx].value = value;
    inputs[idx].disabled = true;
    inputs[idx].classList.add('hinted');
    hintCount++;
    updateHintDisplay();
    document.getElementById('message').innerText = '';
    
    // Trigger conflict detection for the hinted cell
    const currentBoard = getCurrentBoard();
    const conflicts = getConflictingCells(currentBoard, row, col, value);
    clearConflictHighlighting();
    if (conflicts.length > 0) {
      applyConflictHighlighting(row, col, conflicts);
    }
  }
}

async function newGame() {
  const res = await fetch(`/new?difficulty=${currentDifficulty}`);
  
  if (!res.ok) {
    const data = await res.json();
    document.getElementById('message').innerText = data.error || 'Error loading puzzle';
    return;
  }
  
  const data = await res.json();
renderPuzzle(data.puzzle);
document.getElementById('message').innerText = '';
resetHintCount();
startTimer();
  
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = inputs[idx].value;
      board[i][j] = val ? parseInt(val, 10) : 0;
    }
  }
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = '#d32f2f';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    if (inp.disabled) continue;
    inp.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      inp.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
  stopTimer();

  msg.style.color = '#388e3c';
  msg.innerText = 'Congratulations! You solved it!';

  const playerName = window.prompt(
    'Congratulations! Enter your name for the scoreboard:'
  );

  if (playerName && playerName.trim()) {
    addScore(playerName);
  }
} else {
  msg.style.color = '#d32f2f';
  msg.innerText = 'Some cells are incorrect.';
}

}

// Wire buttons
window.addEventListener('load', () => {
  // Difficulty selector
  document.querySelectorAll('.difficulty-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      setDifficulty(btn.dataset.difficulty);
    });
  });
  
  // Game buttons
  document.getElementById('new-game').addEventListener('click', newGame);
  document.getElementById('hint').addEventListener('click', requestHint);
  document.getElementById('check-solution').addEventListener('click', checkSolution);
  
  // Initialize with default difficulty
  renderScoreboard();
  newGame();
});