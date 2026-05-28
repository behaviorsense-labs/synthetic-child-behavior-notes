# Dataset Schema

This document describes the planned fields for the Synthetic Child Behavior Notes dataset.

## Fields

| Field | Description |
|---|---|
| `id` | Unique row identifier |
| `dataset_version` | Dataset release version, such as `v1` |
| `observation_text` | Synthetic caregiver-style behavior observation |
| `age_group` | Approximate child age group, such as `3-5`, `6-8`, `9-12` |
| `setting` | Context where the behavior occurred, such as home, school, public place, therapy preparation, or playground |
| `antecedent` | What happened before the observed behavior |
| `behavior` | Observable behavior described in the note |
| `consequence` | What happened after the behavior, if included |
| `consequence_present` | Whether the consequence is clearly present: `yes` or `no` |
| `possible_trigger` | Possible non-diagnostic trigger or context |
| `emotion_context` | Possible emotional context, such as frustration, anxiety, overwhelm, or tiredness |
| `caregiver_response` | What the caregiver did, if mentioned |
| `suggested_followup_question` | A caregiver-friendly question to clarify the observation |
| `general_support_idea` | General educational support idea, not a treatment recommendation |
| `category` | Behavior context category |
| `risk_level` | General scenario risk label, such as `low`, `moderate`, or `high` |
| `difficulty_level` | Complexity of the example: `easy`, `medium`, or `complex` |
| `ambiguity_level` | How clear or unclear the observation is: `low`, `medium`, or `high` |
| `split` | Dataset split: `train`, `validation`, or `test` |
| `synthetic_flag` | Always `yes` |
| `review_status` | Validation/review status for the row |

## Important Notes

- This dataset is synthetic.
- It does not contain real child, caregiver, school, therapy-session, patient, or clinical data.
- Fields such as `possible_trigger` and `general_support_idea` are educational and non-diagnostic.
- This dataset is not intended for diagnosis, treatment recommendation, clinical decision-making, or risk scoring.
