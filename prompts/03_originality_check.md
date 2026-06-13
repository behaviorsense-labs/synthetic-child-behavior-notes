# Originality and Public-Source Similarity Check

Review the following synthetic child behavior dataset rows.

These rows should be original synthetic examples. They should not be copied from public datasets, papers, websites, therapy documents, school documents, or clinical notes.

## Check For

- Rows that sound copied from a public source
- Rows that sound too polished or clinical
- Rows that sound like real private records
- Rows with overly specific details that could identify a real person or place
- Rows that are too similar to each other (near-duplicates)
- Rows that sound like therapy manual examples or school incident reports
- Rows that use diagnostic terminology (e.g. ADHD, autism, sensory processing disorder) — these should be flagged even if used casually

## Acceptable

Generic caregiver-style wording is fine.

Examples:

- "My child cried when screen time ended."
- "My child refused to start homework."
- "My child covered their ears when the store became loud."

Generic or simple wording is not a concern. Only flag if the row appears non-original or too clinical.

## Near-Duplicate Check

Compare each row's `observation_text`, `antecedent`, and `behavior` fields. Flag any pair where two rows describe essentially the same scenario, even if the wording is slightly different.

## Flag Only If

The row seems copied, overly specific, unusually formal, uses diagnostic language, or is too close to another row in the batch.

## Output Format

For each concern found, return:

```
Row ID:
Concern:
Suggested rewrite:
```

If no concerns are found, say:

```
No originality concerns found in this batch.
```
