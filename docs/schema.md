# Dataset Schema

This file explains the columns planned for the Synthetic Child Behavior Notes dataset.

## Main Fields

| Field | Meaning |
|---|---|
| `id` | Unique number for each row |
| `dataset_version` | Dataset version, such as `v1` |
| `observation_text` | A synthetic caregiver-style note |
| `age_group` | Child age group, such as `3-5`, `6-8`, or `9-12` |
| `setting` | Where the situation happened, such as home, school, playground, or public place |
| `antecedent` | What happened before the behavior |
| `behavior` | What the child did that can be observed |
| `consequence` | What happened after the behavior, if mentioned |
| `consequence_present` | `yes` or `no` |
| `possible_trigger` | A possible context or trigger, not a diagnosis |
| `emotion_context` | Possible emotional context, such as frustration, tiredness, or overwhelm |
| `caregiver_response` | What the caregiver did, if mentioned |
| `suggested_followup_question` | A simple question a caregiver may ask to better understand the note |
| `general_support_idea` | A general support idea, not a treatment recommendation |
| `category` | Type of situation, such as screen-time ending, homework frustration, or sensory overload |
| `risk_level` | General scenario label: `low`, `moderate`, or `high` |
| `difficulty_level` | How complex the example is: `easy`, `medium`, or `complex` |
| `ambiguity_level` | How clear the note is: `low`, `medium`, or `high` |
| `split` | Dataset split: `train`, `validation`, or `test` |
| `synthetic_flag` | Always `yes` |
| `review_status` | Review status for the row |

## Notes

This dataset is fully synthetic. It does not include real child, caregiver, school, therapy, patient, or clinical data.

The dataset is for educational and research prototyping only. It is not for diagnosis, treatment, clinical decisions, or replacing professionals.
