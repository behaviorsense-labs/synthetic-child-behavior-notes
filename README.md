# Synthetic Child Behavior Notes

**Important: This is NOT clinical data.**

This dataset contains fully synthetic child behavior observation notes generated using AI models with human review, editing, validation, and safety checks.

No real child, caregiver, school, therapy-session, patient, or clinical data is included.

## Purpose

This dataset is designed for privacy-safe research and educational prototyping around:

- caregiver note organization
- ABC behavior note structuring
- child behavior category classification
- therapy-session preparation
- follow-up question generation
- caregiver-support AI prototypes

## Dataset Roadmap

- **v1:** 300 synthetic examples
- **v2:** 1,000 synthetic examples
- **v3:** 5,000 synthetic examples

## Planned Dataset Fields

- `id`
- `dataset_version`
- `observation_text`
- `age_group`
- `setting`
- `antecedent`
- `behavior`
- `consequence`
- `consequence_present`
- `possible_trigger`
- `emotion_context`
- `caregiver_response`
- `suggested_followup_question`
- `general_support_idea`
- `category`
- `risk_level`
- `difficulty_level`
- `ambiguity_level`
- `split`
- `synthetic_flag`
- `review_status`

## Intended Use

This dataset may be useful for:

- ABC extraction experiments
- behavior category classification
- caregiver note summarization
- therapy-session brief generation
- privacy-safe AI prototyping
- educational NLP experiments

## Not Intended For

This dataset is not intended for:

- diagnosis
- treatment recommendation
- clinical decision-making
- risk scoring
- replacing therapists, teachers, doctors, or qualified professionals

## Validation Plan

Each dataset release will include validation checks for:

- required fields
- duplicate records
- category balance
- allowed label values
- missing values
- privacy and PII safety
- rule-based consistency
- AI-assisted quality review
- manual sample review

## Disclaimer

This dataset is provided for educational and research prototyping purposes only. It does not provide medical advice, diagnosis, treatment, or clinical decision-making.
