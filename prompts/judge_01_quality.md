# LLM Judge — Quality Scoring

You are evaluating rows from a synthetic child behavior observation dataset.
This dataset is designed for caregiver-support AI research. It is not clinical data.

## Your Task

Score each row on the following 4 dimensions. Use a scale of 1 to 5.

### Scoring Dimensions

**1. Observation Clarity** — Is the observation_text clear and easy to understand from a caregiver's perspective?
- 1 = Very unclear or confusing
- 3 = Understandable but could be clearer
- 5 = Clear, natural caregiver language

**2. Behavior Specificity** — Does the behavior field describe a specific, observable action?
- 1 = Too vague (e.g. "got upset")
- 3 = Somewhat specific
- 5 = Clearly observable and specific action

**3. Category Fit** — Does the category accurately match the described scenario?
- 1 = Wrong category
- 3 = Loosely fits
- 5 = Perfect fit

**4. Language Authenticity** — Does the row sound like real caregiver language, not clinical or academic?
- 1 = Sounds clinical or copied
- 3 = Mostly caregiver-like
- 5 = Authentic caregiver voice

## Output Format

Return a markdown table with exactly these columns:

| row_id | category | observation_clarity | behavior_specificity | category_fit | language_authenticity | average_score | notes |
|--------|----------|--------------------|--------------------|--------------|----------------------|---------------|-------|

- average_score = mean of the 4 scores, rounded to 1 decimal place
- notes = one short phrase only if there is a specific concern, otherwise leave blank
- Do not include any text before or after the table
- Do not explain your scores
