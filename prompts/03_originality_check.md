
---

# 3. `prompts/03_originality_check.md`

**Purpose:** Use this to check whether rows look copied or too similar to public examples.

```markdown
# Originality and Public-Source Similarity Check

Review the following synthetic child behavior dataset rows.

These rows should be original synthetic examples. They should not be copied from public datasets, papers, websites, therapy documents, school documents, or clinical notes.

## Check For

- Rows that sound copied from a public source
- Rows that sound too polished or clinical
- Rows that sound like real private records
- Rows with overly specific details
- Rows that are too similar to each other
- Rows that sound like therapy manual examples or school incident reports

## Acceptable

Generic caregiver-style wording is okay.

Examples:

- "My child cried when screen time ended."
- "My child refused to start homework."
- "My child covered ears when the store became loud."

Generic wording is not a problem.

## Flag Only If

The row seems copied, overly specific, unusually formal, too clinical, or too close to another row.

## Output Format

```text
Row ID:
Concern:
Suggested rewrite:

If no concerns are found, say:

No originality concerns found in this batch.