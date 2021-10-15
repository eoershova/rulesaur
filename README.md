# rulesaur :crocodile:
3 GEC tasks 


HOW TO SET UP AND USE RULESAUR

1) Clone this rep

```$ git clone git@github.com:eoershova/rulesaur.git```

2) Go there

```$ cd rulesaur```

3) Install poetry (you can skip this step if you already have it) code below is for osx / linux / bashonwindows, you can see instructions for other os [here](https://python-poetry.org/docs/)

``` $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - ```

3) Activate poetry

```$ source $HOME/.poetry/env```

4) Install required libraries (just 2 of them: spacy and parameterized)

```$ poetry install```

5) Download spacy model (you can skip this step, just make sure your "en_core_web_sm" is compatible

```$ poetry run python -m spacy download en_core_web_sm```

6) You are ready to go! Choose the task and run it

```$ poetry run python task_1.py```
