# Manual Review Checklist

Use this checklist when reviewing dataset rows before release.

## Row-Level Review

For each row, confirm:

- [ ] Row is fully synthetic — no real people, places, or records
- [ ] No real names, phone numbers, emails, addresses, school names, clinic names, or exact dates
- [ ] Simple caregiver-style wording — not clinical, not formal
- [ ] No diagnosis, treatment, or medical advice language
- [ ] No diagnostic terms or condition names anywhere in the row — not even casually (e.g. ADHD, autism, sensory processing disorder, ODD, anxiety disorder)
- [ ] Category matches the described observation
- [ ] Antecedent describes what happened immediately before the behavior
- [ ] Behavior is observable and specific
- [ ] Consequence is supported by the observation
- [ ] If `consequence_present` is `yes`, consequence field has a specific outcome (not vague)
- [ ] If `consequence_present` is `no`, consequence field reflects that
- [ ] `general_support_idea` is general and non-clinical
- [ ] `suggested_followup_question` is parent-friendly
- [ ] `difficulty_level` is reasonable for the scenario
- [ ] `ambiguity_level` is reasonable for the scenario
- [ ] `risk_level` is appropriate — `high` only if the caregiver described strong safety concern in that moment (e.g. child ran away in a crowded place, refused to stay near caregiver) — no injury descriptions or clinical framing
- [ ] Row does not sound copied from a public source
- [ ] Row is not a near-duplicate of another row

## Schema Compliance Check

- [ ] `dataset_version` = `v2`
- [ ] `age_group` is one of: `3-5`, `6-8`, `9-12`
- [ ] `setting` is one of: `home`, `school-classroom`, `school-playground`, `public-store`, `public-restaurant`, `public-transport`, `outdoor`, `daycare`, `relative-home`, `other-public`
- [ ] `consequence_present` is `yes` or `no`
- [ ] `risk_level` is one of: `low`, `moderate`, `high`
- [ ] `difficulty_level` is one of: `easy`, `medium`, `complex`
- [ ] `ambiguity_level` is one of: `low`, `medium`, `high`
- [ ] `split` is one of: `train`, `validation`, `test`
- [ ] `synthetic_flag` = `yes`
- [ ] `review_status` = `draft`

## Batch-Level Distribution Check

After reviewing all rows in a batch, verify approximate distributions:

| Field | Target | Actual |
|---|---|---|
| age_group: 3-5 | ~25% | |
| age_group: 6-8 | ~40% | |
| age_group: 9-12 | ~35% | |
| difficulty_level: easy | ~25% | |
| difficulty_level: medium | ~50% | |
| difficulty_level: complex | ~25% | |
| ambiguity_level: low | ~40% | |
| ambiguity_level: medium | ~40% | |
| ambiguity_level: high | ~20% | |
| risk_level: low | ~60% | |
| risk_level: moderate | ~30% | |
| risk_level: high | ~10% | |
| consequence_present: yes | ~30% | |
| split: train | ~60% | |
| split: validation | ~15% | |
| split: test | ~25% | |

## Batch Notes

```
Batch name:
Category:
Row ID range:
Rows reviewed:
Rows corrected:
Rows removed:
Main issues found:
Distribution concerns:
Status: draft / reviewed / approved
```
