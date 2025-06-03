# typeform-yaml

This repository contains code to define Typeform survey using yaml, 
this is _explicitely_ a small subset of typeforms features. 

The goal is to be able to have collaborative editing of survey as yaml on 
GitHub and to _easily_ repeat and update those survey through time. 

Thus the Yaml must be fairly readable and minimal as anyway open-source maintainer 
can't spend an inordinate amount of time making too complicated surveys. 

This only implement a small subset of Typeform.

## YAML format

The basic structure is
```yaml
id: 'abcdefg'
title: 'The survey title'
questions:
  # list of questions
```

### Questions

Each question is a dict with keys

```yaml
questions:
  - title: 'The qustion title'
    description: |
      An optional possibly longer description
    type: type
```

The following question types are supported

#### statement

No questions, just a statement with "Continue", e.g.
```yaml
  - title: 'Thanks for your participation'
    type: statement
    description: |
        See <link> to get updates on the survey results.
```

#### number
A single number, e.g.
```yaml
  - title: 'How many years have you been using Python?'
    type: number
```

#### long_text
A freeform multiline text, e.g.
```yaml
  - title: 'What do you like most about Python?'
    type: long_text
```

#### multiple_choices
Select one or more answers, e.g.

```yaml
  - title: 'What is your favorite fruit?'
    choices:
      - 'Apple'
      - 'Pineapple'
```

The `type: multiple_choices` specification is optional and automatically set if `choices` is in the question.

Possible modifiers:
- Add `multiple: true` to the question to allow multiple answers.
- Add `other: true` to the question or `::other_please_type::` to the `choices` to add a choice "Other"
  with a text field. If you want the choice "Other" without a text field, simply put the string "Other"
  as choice.

#### ranking
Sort answers by priority
```yaml
  - title: 'Sort these fruits by deliciousness'
    type: ranking
    choices:
      - 'Apple'
      - 'Pineapple'
      - 'Lemon'
```

#### option_scale

```yaml
  - title: 'Rate this survey'
    type: option_scale
    start: 0  # start of scale: must be 0 or 1, optional, default: 0
    steps: 11 # the number of steps, optional, default: 11
    labels: ['not helpful', 'very good']  # optional list of strings
    # (left, [middle], right) label of the scale
```

#### yes_no_jump

Yes/no question influcencing control flow. TODO