# Review Synthetic Dataset Rows

Review the following synthetic child behavior dataset rows.

The dataset is for caregiver-support AI research and educational prototyping. It is not clinical data.

## Check Each Row For

- Is the row fully synthetic?
- Does it avoid real names, phone numbers, emails, addresses, school names, clinic names, and exact dates?
- Does it avoid diagnosis, treatment advice, clinical decision-making, and medical advice?
- Does it avoid all diagnostic terms and condition names — even used casually (e.g. ADHD, autism, sensory processing disorder, ODD, anxiety disorder, or any similar label)?
- Is the wording simple and caregiver-like?
- Does the category match the observation?
- Does the antecedent describe what happened before the behavior?
- Is the behavior observable and specific?
- Is the consequence supported by the observation?
- Is the support idea general and safe, not clinical?
- Is the row too similar to another row in the batch?

## Check Schema Compliance

- `dataset_version` must be `v2`
- `age_group` must be one of: `3-5`, `6-8`, `9-12`
- `setting` must be one of: `home`, `school-classroom`, `school-playground`, `public-store`, `public-restaurant`, `public-transport`, `outdoor`, `daycare`, `relative-home`, `other-public`
- `consequence_present` must be `yes` or `no`
- If `consequence_present` is `yes`, the `consequence` field must describe a specific observable outcome — not a vague phrase like "Not clearly mentioned"
- If `consequence_present` is `no`, the `consequence` field should reflect that nothing specific was noted
- `risk_level` must be one of: `low`, `moderate`, `high`
- `difficulty_level` must be one of: `easy`, `medium`, `complex`
- `ambiguity_level` must be one of: `low`, `medium`, `high`
- `split` must be one of: `train`, `validation`, `test`
- `synthetic_flag` must be `yes`
- `review_status` must be `draft`

## Flag Any Row That

- Sounds copied from a public source
- Sounds too clinical or uses diagnostic terminology
- Sounds too specific or private
- Uses judgmental or stigmatizing wording
- Has the wrong category for the described behavior
- Has a field value outside the allowed values above
- Has `consequence_present: yes` with a vague or empty consequence
- Has awkward or unnatural caregiver wording

## Output Format

For each issue found, return:

```
Row ID:
Field:
Issue:
Suggested correction:
```

If no issues are found, say:

```
No issues found in this batch.
```
