# typeform-yaml-survey

This repository contains code to define Typeform surveys using yaml.
This is _explicitly_ a small subset of typeforms features.

The goal is to be able to have collaborative editing of surveys as yaml on
GitHub and to _easily_ repeat and update those surveys through time.

Thus the yaml must be fairly readable and minimal as open-source maintainers
can't spend an inordinate amount of time making overly complicated surveys.

This only implements a small subset of Typeform.

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

The following question types are supported:

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
  as choice. If you want to change the label of the "Other" choice, navigate to the Typeform survey
  settings and edit the label in the "Language" tab.

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

## How to integrate with Typeform

After creating a Typeform account, you can create a new survey and then copy the `form_id` from the URL of the survey. For example if the URL is `https://admin.typeform.com/form/abc123/edit`, then the `form_id` is `abc123`.

Click on your profile icon in the top right corner, then "Your settings", and "Personal tokens". Click on "Generate a new token" and give it a name. Next, copy the token and create and environment variable called `TYPEFORM_TOKEN`. This environment variable will be used by the code to authenticate with the Typeform API. You can then run the code to create the survey using the `form_id` and the `TYPEFORM_TOKEN` environment variable.

