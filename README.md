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
1. To be as the only verb. I am tired. -> I am not tired.
2. Lexical negation for sentences with everyone|everybody. Everyone likes cats -> No one likes cats.
3. Auxiliary verb as the only verb. I should. -> I shouldn't.
4. Sentence with lexical verb only. I swim. -> I don't swim.
5. Sentence with both lexical verb and auxiliary verbs. I will have finished by Sunday -> I won't have finished by Sunday.
6. Sentences with I wish + past simple. I wish I could play piano -> I wish I couldn't play piano.



Alongside those strategies work additional mappings that ensure the sentence remains grammatically correct:
1. Mapping between some|somebody|something any|anybody|anything depending on their syntax. I have some apples -> I don't have any apples. BUT Some people like cats -> Some people don't like cats.
2. Mapping between too and either.



TASK 2

For this task I developed a general detector pattern that could identify NSUBJ groups with their verbs. After detection I checked the verb's forms, I prohibited sentences with verbs in present tense, non singular number or past tense form of to be in singular. Every other sentence I allowed as it is not always possible to determine verb number in past tense form. This task has designated tests that can be run with.

```$ poetry run python tests/test_task_2.py```

In the tests one can see the cases that can be handled and exceptions caused by spacy tagger mistakes. 

TASK 3

According to the description of the task one had to identify cases when auxiliary verb was applied not to base form of the lexical verb and it caused the sentence to be ungrammatical. This was the hardest part, for auxiliary verb can applied not only to base form without causing errors. Inspired by REALEC, I developed 3 patterns for possible variations of the error:

1. Auxiliary + non base form. This pattern detects all instances, checks finite verb form, if it is incomparable with the auxiliary (several auxiliaries are possible to process withing one sentence). Like in "It should been approved.".
2. Auxiliary + (base form and non base form). This pattern takes into consideration that one auxiliary can be applied to two verbs while being a direct descendant of only one of them. Consider the sentence "It will be safe and looks amazing."
3. Auxiliary + auxiliary. For example, "I didn't can".

This task also has designated tests that can be run with.

```$ poetry run python tests/test_task_3.py```


POSSIBLE IMPROVEMENTS

TASK 1
1) More strategies for complex constructions like "I'd rather you stayed at home" or sentences containing "only" that will most likely need word reordering.
2) Condition for "too" to be remapped to "either" only in cases like "I don't like ducks either" and not "I don't like ducks too much".
3) Negating verbs like "think" with "think not" and not "don't think"

TASK 2
1) Pattern to infer verb number in past tense from the context.

TASK 3
1) Filter for Aux + Aux pattern as it can be correct as well, consider "Do not imagine, Miss Bennet, that your ambition will ever be gratified."

COMMENTS ON TECHICAL EXECUTION

I used spacy and nothing else for constructing patterns and making transformation and filter pipelines. One library for everything: pos tagging, fine-grained morphology tagging, syntactic parsing. Spacy was also useful for extracting lemmas.


All tasks follow the same template:
1) Processing input and constructing doc
2) Setting custom attributes to sents in doc. That's where I stored "is_target" label and negated forms of sentences.
3) Assembling patterns into Matcher. I completed patterns with on match callbacks to allow for asynchronous processing withing pipelines. 
4) Matching and running callbacks to process sents
5) In case of task one, first Matcher is used to filter out sentences that cannot be securely negated and second Matcher is used for determining the best negation strategy and using it.
6) task_2 and task_3 store their results in .json files to be later used for testing. In order to run on testing data use 
```$ poetry run python task_2```
```tests/data/raw_data/task_3_test_data.txt```

Thanks for reading till here! :zap:





