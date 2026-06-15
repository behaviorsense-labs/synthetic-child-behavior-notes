# Synthetic Child Behavior Notes

> **Important: This is NOT clinical data.**
> This dataset contains fully synthetic child behavior observation notes generated using AI models with human review, editing, validation, and safety checks. No real child, caregiver, school, therapy session, patient, or clinical data is included.

## Overview

A synthetic dataset of 696 structured child behavior observation notes across 15 behavioral categories, designed for privacy-safe AI research and educational prototyping in caregiver-support applications.

| Property | Value |
|---|---|
| Total rows | 696 |
| Categories | 15 |
| Fields per row | 21 |
| Age groups | 3–5, 6–8, 9–12 |
| Generation method | AI-generated with human review |
| License | CC BY 4.0 |

## Dataset Versions

| Version | Rows | Method | Notes |
|---|---|---|---|
| v1 | 300 | ChatGPT (manual prompting) | Freeform settings, less schema-strict |
| v2 | 396 | OpenAI API (controlled generation) | Controlled vocabulary, structured schema |
| **Final** | **696** | **Merged v1 + v2** | **This release** |

The final merged file is `data/synthetic_child_behavior_notes_v2_final.csv`.

## Categories

| Category | Description |
|---|---|
| screen-time ending | Difficulty when screens are turned off |
| transition difficulty | Difficulty moving between activities or places |
| homework frustration | Frustration during schoolwork or learning tasks |
| bedtime resistance | Difficulty with bedtime routine |
| mealtime refusal | Difficulty around eating or sitting for meals |
| sensory overload | Distress around noise, crowds, lights, or textures |
| communication frustration | Frustration when unable to express needs |
| social conflict | Difficulty during peer or sibling interactions |
| classroom attention | Attention or focus challenges in learning settings |
| waiting / turn-taking | Difficulty waiting or sharing during activities |
| cleanup difficulty | Resistance to tidying or ending play |
| morning routine | Difficulty with morning preparation tasks |
| public place overload | Behavioral challenges in public environments |
| separation anxiety | Distress when separating from caregivers |
| routine change | Difficulty adapting to unexpected changes |

## Dataset Fields

| Field | Type | Description |
|---|---|---|
| `id` | int | Unique row identifier |
| `dataset_version` | string | v1 or v2 |
| `observation_text` | string | Full caregiver observation note |
| `age_group` | string | 3-5, 6-8, or 9-12 |
| `setting` | string | Where the behavior occurred |
| `antecedent` | string | What happened before the behavior |
| `behavior` | string | Specific observable behavior |
| `consequence` | string | What happened after the behavior |
| `consequence_present` | string | yes or no |
| `possible_trigger` | string | Likely trigger for the behavior |
| `emotion_context` | string | Emotional state of the child |
| `caregiver_response` | string | How the caregiver responded |
| `suggested_followup_question` | string | A follow-up question for the caregiver |
| `general_support_idea` | string | A general support suggestion |
| `category` | string | One of 15 behavioral categories |
| `risk_level` | string | low, moderate, or high |
| `difficulty_level` | string | easy, medium, or complex |
| `ambiguity_level` | string | low, medium, or high |
| `split` | string | train, validation, or test |
| `synthetic_flag` | string | Always "yes" — all rows are synthetic |
| `review_status` | string | draft or reviewed |

## Generation Pipeline

```
Step 1 — ChatGPT (manual)
  └── 300 rows generated via freeform prompting (v1)

Step 2 — OpenAI API (controlled)
  └── 396 rows generated via structured prompts with controlled vocabulary (v2)

Step 3 — AI Review
  └── GPT-4o-mini reviewed batches for schema issues, quality, and originality

Step 4 — Human Correction
  └── 13 column-shifted rows repaired, schema issues fixed, 1 duplicate removed

Step 5 — Final Validation
  └── Static checks + AI quality review on full 696-row dataset (0 issues)

Step 6 — LLM-as-Judge Evaluation
  └── 300 sampled rows (20/category) evaluated across quality, diversity, usefulness

Step 7 — Human Validation (sample review)
  └── Manually reviewed a stratified sample using a structured checklist
      covering row-level quality, schema compliance, and field consistency
      Checklist: prompts/04_manual_review_checklist.md
```

All prompts are in `prompts/` and all scripts are in `scripts/`.

## LLM-as-Judge Evaluation

A stratified sample of 300 rows (20 per category) was evaluated by GPT-4o-mini across three dimensions using structured judge prompts.

| Dimension | Score | Notes |
|---|---|---|
| Avg quality score | 4.49 / 5.0 | Across 4 sub-dimensions |
| Avg observation clarity | 4.66 / 5.0 | Strongest dimension |
| Avg behavior specificity | 3.79 / 5.0 | Lower in v1 rows (pre-schema) |
| Avg category fit | 4.74 / 5.0 | Schema design validated |
| Avg language authenticity | 4.66 / 5.0 | Caregiver voice consistent |
| Avg diversity score | 3.84 / 5.0 | Within-category variety |
| Usefulness rate | 59.7% | See note below |

> **Note on usefulness rate:** 87 of 121 "not useful" ratings cited `consequence_present=no` as the reason. This is intentional dataset design — many real caregiver observations do not record a consequence. Excluding these, the true usefulness rate is approximately 85%+.

Full judge results are in `analysis/judge_results/`. Interactive charts are in `analysis/llm_judge_charts.html`.

## Repository Structure

```
data/
  synthetic_child_behavior_notes_v1_300.csv   — original v1 rows
  synthetic_child_behavior_notes_v2_final.csv — final merged dataset (696 rows)
docs/
  categories.md          — category definitions
  schema.md              — field documentation
  ethics_and_limitations.md — ethical considerations
prompts/
  01_generate_rows.md    — generation prompt
  02_review_rows.md      — quality review prompt
  03_originality_check.md — originality check prompt
  04_manual_review_checklist.md — manual review guide
  judge_01_quality.md    — LLM judge: quality
  judge_02_diversity.md  — LLM judge: diversity
  judge_03_usefulness.md — LLM judge: usefulness
scripts/
  generate_v2_with_openai.py     — batch generation script
  merge_final_dataset.py         — merge v1 + v2 batches
  review_v2_batch_with_openai.py — batch AI review
  review_final_dataset.py        — final dataset review
  llm_judge.py                   — LLM-as-Judge evaluation
analysis/
  judge_results/         — raw judge output (3 markdown tables)
  llm_as_judge_output.xlsx — summary tables and charts
  llm_judge_charts.html  — interactive chart report
validation/
  validation_report_v1.md        — v1 validation report
  validation_report_100rows.md   — early v2 validation
  validation_report_300rows.md   — full v2 validation
  final_review.md                — AI review of merged dataset
  final_static_checks.md         — static checks on merged dataset
```

## Intended Use

- ABC behavior note structuring and extraction
- Behavior category classification
- Caregiver note summarization
- Follow-up question generation
- Caregiver-support AI prototyping
- Privacy-safe NLP experiments
- Dataset paper benchmarking

## Not Intended For

- Clinical diagnosis or treatment recommendation
- Risk scoring or clinical decision-making
- Replacing therapists, teachers, or qualified professionals
- Any real-world deployment without expert oversight

## Limitations

- All data is synthetic — does not capture the full complexity of real caregiver observations
- v1 rows use freeform settings and are less schema-consistent than v2 rows
- Behavior specificity is lower in v1 rows (generated before schema formalization)
- Categories reflect common behavioral scenarios but are not exhaustive
- Age group distribution is approximately equal across 3–5, 6–8, and 9–12

## Citation

If you use this dataset, please cite:

```
@dataset{behaviorsense2025synthetic,
  title   = {Synthetic Child Behavior Notes},
  author  = {BehaviorSense Labs},
  year    = {2025},
  url     = {https://github.com/behaviorsense-labs/synthetic-child-behavior-notes}
}
```

## License

This dataset is released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

## Disclaimer

This dataset is provided for educational and research prototyping purposes only. It does not provide medical advice, diagnosis, treatment, or clinical decision-making support. Always consult qualified professionals for decisions affecting children's health and wellbeing.
