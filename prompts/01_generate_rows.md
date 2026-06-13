# Generate Synthetic Dataset Rows

Generate synthetic child behavior observation rows for the Synthetic Child Behavior Notes dataset.

## Category

CATEGORY_NAME_HERE

## Number of Rows

NUMBER_OF_ROWS_HERE

## Row IDs

START_ID_HERE to END_ID_HERE

## Rules

- All rows must be synthetic.
- Do not copy from public datasets, websites, articles, therapy guides, school documents, or clinical examples.
- Do not include real names, phone numbers, emails, addresses, school names, clinic names, or exact dates.
- Do not include diagnosis, treatment advice, clinical decision-making, risk scoring, or medical advice. If a behavior could suggest a condition, describe only the observable behavior — never name or imply a diagnosis.
- Do not use any diagnostic terms, condition names, or clinical labels (e.g. do not write ADHD, autism, sensory processing disorder, ODD, anxiety disorder, or any similar term — not even casually or as a possible explanation).
- Use simple caregiver-style wording.
- Keep the examples parent-friendly and non-clinical.
- Use only the requested category.
- Use `general_support_idea`, not intervention or treatment.

## Required Distributions

Spread rows across the following values. Do not cluster all rows into the same value.

**age_group** — use all three groups:
- 3-5: approximately 25% of rows
- 6-8: approximately 40% of rows
- 9-12: approximately 35% of rows

**setting** — use only these allowed values (pick the most realistic for the scenario):
- home
- school-classroom
- school-playground
- public-store
- public-restaurant
- public-transport
- outdoor
- daycare
- relative-home
- other-public

**difficulty_level** — vary across all three:
- easy: approximately 25% of rows
- medium: approximately 50% of rows
- complex: approximately 25% of rows

**ambiguity_level** — vary including high:
- low: approximately 40% of rows
- medium: approximately 40% of rows
- high: approximately 20% of rows

**risk_level** — include all three levels:
- low: approximately 60% of rows
- moderate: approximately 30% of rows
- high: approximately 10% of rows

For `risk_level: high`, use scenarios where the caregiver expressed strong concern about the child's safety in that moment. Use a variety of distinct patterns — do not repeat the same scenario structure across rows. Choose from different patterns such as:
- Child leaving a safe space or moving away from the caregiver in a crowded area
- Child refusing to come inside from an outdoor space after repeated requests
- Child throwing or knocking over objects near other people
- Child locking or barricading a door so the caregiver cannot check on them
- Child climbing to an unsafe height during a transition

Each high-risk row must use a different pattern. Do not write more than one row with the same core scenario. Keep wording non-clinical, caregiver-style, and fully synthetic. Do not use diagnostic language, injury descriptions, or clinical risk framing.

For `risk_level: moderate`, at least 25% of rows in the batch must be moderate. Do not skip moderate in favour of only low and high.

**consequence_present** — vary:
- no: approximately 70% of rows
- yes: approximately 30% of rows

For `consequence_present: yes` — the `consequence` field must describe a specific observable outcome: what the child did next, what changed, or what the caregiver observed as a result. Good examples:
- "Child placed the tablet on the shelf and went to get a snack."
- "Child calmed down after caregiver offered two choices and picked drawing."
- "Child handed the phone back and sat quietly at the table."
Do NOT use vague phrases like "Cried and pouted", "Calmed after a short while", "Concerned about their safety", "Left the area", or any emotion or action that doesn't describe a clear observable outcome.

For `consequence_present: no` — the `consequence` field must be exactly: `No consequence noted`

**split** — assign as follows:
- train: 60% of rows
- validation: 15% of rows
- test: 25% of rows

## Schema

```csv
id,observation_text,age_group,setting,antecedent,behavior,consequence,consequence_present,possible_trigger,emotion_context,caregiver_response,suggested_followup_question,general_support_idea,category,risk_level,difficulty_level,ambiguity_level,split
```

**Allowed values per field:**

| Field | Allowed Values |
|---|---|
| age_group | 3-5, 6-8, 9-12 |
| setting | home, school-classroom, school-playground, public-store, public-restaurant, public-transport, outdoor, daycare, relative-home, other-public |
| consequence_present | yes, no |
| risk_level | low, moderate, high |
| difficulty_level | easy, medium, complex |
| ambiguity_level | low, medium, high |
| split | train, validation, test |

## Output

Return CSV rows including the header row as the first line.

Do not include explanations.

Do not wrap output in code blocks or markdown.

Every row must have a unique `behavior` field. Do not reuse the same behavior description across rows, even in different settings or age groups. The behavior must describe what that specific child did — vary the action, the words used, and the intensity across rows.

Every field must be wrapped in double quotes. Any field containing a comma must also be wrapped in double quotes. Do not add trailing spaces after any value.