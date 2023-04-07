# Hookshot-survivor

Hookshot Survivor is a gamejam project over easter 2023. It is our first interactions with the 3d game engine Ursina.

### Setting up Hookshot-survivor for development/testing

Project dependencies are managed with Poetry. [Install Poetry](https://python-poetry.org/docs/).

In a command prompt:

1. Check you have poetry with `poetry --version`
2. Navigate to this project directory `cd /path/to/git/repo`
3. Run `poetry install` to install/update your virtual environment (Does nothing if your venv is already up to date).
4. Run `poetry shell` to enter project virtual environment.
5. Run `pre-commit install` to add code checking/fixing on commit
6. Run `./main` to begin the game



### Running the game

Ensure you've set up the game before on this computer.

1. Navigate to this project directory `cd /path/to/git/repo`
2. Run `poetry shell` to enter project virtual environment.
3. Run `./main` to begin the game



### Adding dependencies

If you wish to add a dependency which may normally do via `pip install numpy` then it's as easy as `poetry add numpy`.

Made a mistake? Remove a dependency with `poetry remove numpy`. For more, refer to PyPoetry's documentation.
