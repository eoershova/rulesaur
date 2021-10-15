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



SOLUTION DESCRIPTIONS

TASK 1

In this task, I focused on two things.
Firstly, I made sure that I am adding negations only to sentences that can be negated i.e. they don't have straightforward negations like "cannot", lexical negators like "never" or positive polarity items like "somewhat" that cannot be securely remapped.
Secondly, I tried to determine the best negation strategy for each sentence to make sure the resulting sentence would not be rendered ungrammatical.
I developed separate strategies for 5 types of negation:
1. To be as the only verb. I am -> I am not
2. Lexical negation for sentences with everyone|everybody. Everyone likes cats -> No one likes cats.
3. Auxiliary verb as the only verb. I should -> I shouldn't.
4. Sentence with lexical verb only. I swim -> I don't swim.
5. Sentence with both lexical verb and auxiliary verbs. I will have finished by Sunday -> I won't have finished by Sunday.
6. Sentences with I wish + past simple. I wish I could play piano -> I wish I couldn't play piano.



Alongside those strategies work additional mappings that ensure the sentence remains grammatically correct:
1. Mapping between some|somebody|something any|anybody|anything depending on their syntax. I have some apples -> I don't have any apples. BUT Some people like cats -> Some people don't like cats.
2. Mapping between too and either.



TASK 2






