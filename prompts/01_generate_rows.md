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
- Do not include diagnosis, treatment advice, clinical decision-making, risk scoring, or medical advice.
- Use simple caregiver-style wording.
- Keep the examples parent-friendly and non-clinical.
- Use only the requested category.
- Vary age group, setting, difficulty level, ambiguity level, and consequence presence.
- Use `general_support_idea`, not intervention or treatment.

## Schema

```csv
id,dataset_version,observation_text,age_group,setting,antecedent,behavior,consequence,consequence_present,possible_trigger,emotion_context,caregiver_response,suggested_followup_question,general_support_idea,category,risk_level,difficulty_level,ambiguity_level,split,synthetic_flag,review_status

Allowed Values
dataset_version: v2
consequence_present: yes, no
risk_level: low, moderate, high
difficulty_level: easy, medium, complex
ambiguity_level: low, medium, high
split: train, validation, test
synthetic_flag: yes
review_status: draft
Output

Return only CSV rows.

Do not include the header.

Do not include explanations.