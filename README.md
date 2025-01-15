# typeform-yaml

This repository contains code to define Typeform survey using yaml, 
this is _explicitely_ a small subset of typeforms features. 

The goal is to be able to have collaborative editing of survey as yaml on 
GitHub and to _easily_ repeat and update those survey through time. 

Thus the Yaml must be fairly readable and minimal as anyway open-source maintainer 
can't spend an inordinate amount of time making too complicated surveys. 

This only implement a small subset of Typeform, 

You'll find multiple type of questions, usually defined by a `type: key`

- Multiple choice questions (single|multiple answer possible is the default). 
    - the `other:true`: will add an `Other:` option that let the user type text when selectingl otherwise; just manually
      as an "Other" choice; 

- `type:statement` (no questions, just a statement with "Continue"
- `type:number` let you input a free number
- `opinion_scale` , with 2 or 3 labels (left, [middle], right)
- `long_text` (freeform multiline text)



