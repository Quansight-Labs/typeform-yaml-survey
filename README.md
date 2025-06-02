# typeform-yaml-survey

This repository contains code to define Typeform surveys using yaml.
This is _explicitly_ a small subset of typeforms features.

The goal is to be able to have collaborative editing of surveys as yaml on
GitHub and to _easily_ repeat and update those surveys through time.

Thus the yaml must be fairly readable and minimal as open-source maintainers
can't spend an inordinate amount of time making overly complicated surveys.

You'll find multiple types of questions, usually defined by `type: key`

- Multiple choice questions (single|multiple answers possible is the default).
- The `other:true` option will add an `Other:` response that lets the user type text when selecting it. Otherwise, just manually add an "Other" choice. If you want to change the label of the "Other" choice, navigate to the Typeform survey settings and edit the label in the "Language" tab.
- `type:statement` (no questions, just a statement with "Continue"
- `type:number` let you input a free number
- `opinion_scale` , with 2 or 3 labels (left, [middle], right)
- `long_text` (freeform multiline text)

## How to integrate with Typeform

After creating a Typeform account, you can create a new survey and then copy the `form_id` from the URL of the survey. For example if the URL is `https://admin.typeform.com/form/abc123/edit`, then the `form_id` is `abc123`.

Click on your profile icon in the top right corner, then "Your settings", and "Personal tokens". Click on "Generate a new token" and give it a name. Next, copy the token and create and environment variable called `TYPEFORM_TOKEN`. This environment variable will be used by the code to authenticate with the Typeform API. You can then run the code to create the survey using the `form_id` and the `TYPEFORM_TOKEN` environment variable.
