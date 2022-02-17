# Poetry

[Poetry](https://python-poetry.org/docs/) covers three common Python hurdles: dependencies, virtual environments (`venv`), and packaging.

For `scriptorium`'s use case, it generates the `venv` and `requirements.txt`, respectively.

## Usage
```bash
# Install
curl -sSL https://install.python-poetry.org | $(which python3) -

# Change config
poetry config virtualenvs.in-project true           # .venv in `pwd`

# Activate virtual environment (venv)
poetry shell

# Deactivate venv
exit  # ctrl-d

# Install multiple libraries
poetry add requests inquirer

# Initialize existing project
poetry init

# Run script and exit environment
poetry run scriptorium

# Install from requirements.txt
poetry add `cat requirements.txt`

# Update dependencies
poetry update

# Remove library
poetry remove icecream

# Generate requirements.txt
poetry export -f requirements.txt --output requirements.txt --without-hashes
```

## Alternative to Poetry
It's possible to create a `venv` and `requirements.txt` file with built-in Python and pip.

```bash
# create a virtual environment via python
python3 -m venv .venv

# activate virtual environment
source .venv/bin/activate

# install dependencies
python3 -m pip install requests inquirer

# generate requirements.txt
python3 -m pip freeze > requirements.txt

# exit virtual environment
deactivate
```

## Further Reading
[Basic usage | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/basic-usage/)

[venv — Creation of virtual environments — Python 3.7.2 documentation](https://docs.python.org/3/library/venv.html)

[pip freeze - pip documentation v22.0.3](https://pip.pypa.io/en/stable/cli/pip_freeze/)
