
---

# 2. `prompts/02_review_rows.md`

**Purpose:** Use this after generating a batch. It checks safety and quality.

```markdown
# Review Synthetic Dataset Rows

Review the following synthetic child behavior dataset rows.

The dataset is for caregiver-support AI research and educational prototyping. It is not clinical data.

## Check Each Row For

- Is the row fully synthetic?
- Does it avoid real names, phone numbers, emails, addresses, school names, clinic names, and exact dates?
- Does it avoid diagnosis, treatment advice, clinical decision-making, and medical advice?
- Is the wording simple and caregiver-like?
- Does the category match the observation?
- Does the antecedent describe what happened before the behavior?
- Is the behavior observable?
- Is the consequence supported by the observation?
- Is the support idea general and safe?
- Is the row too similar to another row?

## Flag Any Row That

- Sounds copied from a public source
- Sounds too clinical
- Sounds too specific or private
- Uses judgmental wording
- Has wrong category
- Has unsupported fields
- Has awkward or unnatural wording

## Output Format

For each issue, return:

```text
Row ID:
Issue:
Suggested correction:

If no issues are found, say:

No issues found in this batch.