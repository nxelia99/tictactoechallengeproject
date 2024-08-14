// Function to create a new game
export function createGame() {
    // Send a POST request to create a new game
    fetch('/create', {  
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    // If the response is not okay
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    // If the new game is successfully created, redirect to the game page
    .then(data => {
        if (data.matchId) {
            window.location.href = `/game/${data.matchId}`; 
        } else {
            throw new Error('Failed to create game: No matchId received');
        }
    })
    // Log any errors
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to create game. Please try again.'); // Show an alert to the user
    });
}

let matchId;
let currentTurn;

export async function initGame(id) {
  matchId = id;

  try {
    // Fetch the game state from the new JSON endpoint
    const response = await fetch(`/game/${matchId}/state`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Parse the JSON response
    const data = await response.json();
    console.log('Board:', data.board); // Log the board state

    updateBoard(data.board);  // Update the board with the retrieved state

    // Update the current turn and game status in the UI
    currentTurn = data.currentTurn;  
    document.getElementById('currentTurn').textContent = currentTurn;
    document.getElementById('status').textContent = data.status;
  } catch (error) {
    // Log the errors that may occur during the fetch operation
    console.error('Fetch error:', error);
    // Update the status in the UI to indicate a connection failure
    document.getElementById('status').textContent = "Failed to connect to the server.";
  }

  // Event listener to initialize the game when the window finishes loading
  window.onload = async () => {
    await initGame(matchId);
  };
}

// Function to handle the players' moves
export async function makeMove(x, y) {
    // Send a POST request to the server with the move details
    const response = await fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            matchId: matchId,
            playerId: currentTurn,
            x: x,
            y: y
        }),
    });

    // Parse the JSON response from the server
    const data = await response.json();
    console.log(data)

    // Update the game state if the move was successful
    if (response.ok) {
        updateBoard(data.board);
        currentTurn = data.currentTurn;
        document.getElementById('currentTurn').textContent = currentTurn;
        document.getElementById('status').textContent = data.status;
    } else {
        alert(data.error);
    }
}

// Update the game board in the template
export function updateBoard(board) {
    console.log('Updating board:', board);
    const cells = document.querySelectorAll('.cell');

    board.flat().forEach((value, index) => {
        console.log(`Cell ${index}: ${value}`);
        cells[index].className = 'cell'; // Reset the cell class
        if (value === 'X') {
            cells[index].innerHTML = '&#10008;'; // Set X symbol
            cells[index].classList.add('cell-X');
        } else if (value === 'O') {
            cells[index].innerHTML = '&#9711;'; // Set O symbol
            cells[index].classList.add('cell-O');
        } else {
            cells[index].innerHTML = ''; // Empty cell
        }
    });
}