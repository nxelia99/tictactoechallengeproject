# Tic-Tac-Toe Web Service

This project is an implementation of a web service for the Tic-Tac-Toe game using Python and Flask. I have taken the liberty of adding a basic user interface with HTML and CSS, as well as JS scripts to enhance the experience and functionality. 
I've added various elements that I’ve learned thanks to my personal programming projects over these years. These additions enhance its functionality.

This project is a product of the instructions that I've been given and the knowledge I've gained from personal programming projects over the years. 

## Description

This web service allows users to play Tic-Tac-Toe. It provides endpoints for creating games, making moves, and checking the status of ongoing games.

## Features

- Creation of new games
- Making moves
- Checking the game status
- Automatic determination of the winner or a tie
- Simple web interface for playing

## Technologies used

- Python 3.8+
- Flask
- JS
- SQLAlchemy
- Docker

# Project structure:

```bash
tic_tac_toe/
├── app/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   ├── static/
│   │   ├── css/
│   │   ├── services/
│   ├── templates/
│   ├──__init__.py
│   └── main.py
├── instance/
├── tests/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── README.md

````


## Installation

1. Clone this repository:

```bash
git clone https://github.com/nxelia99/tictactoechallengeproject
```

2. Navigate to the project directory:

```bash
cd tictactoechallengeproject
```

3. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use venv\Scripts\activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the development server:

```bash
python run.py
```

2. Open a browser and go to `http://localhost:5000`

3. Use the API endpoints to interact with the game:
   - GET `/`: Home page that leads to `/create` to start a new game.
   - POST `/create`: Creates a new game:
      http://localhost:5000/create
   - POST `/move`: Makes a move: 
   ```bash
         {
            "board": [
               [
                     "X",
                     " ",
                     " "
               ],
               [
                     " ",
                     "O",
                     " "
               ],
               [
                     " ",
                     " ",
                     " "
               ]
            ],
            "currentPlayer": "X",
            "status": "In progress"
      }
      ````
   - GET `/status`: Retrieves the status of a game: 
      http://localhost:5000/status?matchId=b67de
   - GET `/game/<match_id>`: Starts the match with the given ID:
      http://localhost:5000/game/b67de
   - GET `/game/<match_id>/state`:  Saves the status of the game  in case we refresh the page.  
      

## Testing

To run the tests:

```bash
python -m unittest tests/test_routes.py
python -m unittest tests/test_game_service.py
```

## Deployment with Docker

1. Build the Docker image:

``` bash
docker-compose up --build
```

2. Run the container:

```bash
docker run -p 5000:5000 tictactoechallenge-web
```


Contact me: nxelia99@gmail.com
