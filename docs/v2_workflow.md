# V2 Workflow

This document explains how v2 rows will be created and reviewed.

## Goal

Expand the dataset from 300 rows to 1,000 rows while keeping the data synthetic, simple, caregiver-centered, and non-clinical.

## Process

1. Use the v1 dataset as the seed dataset.
2. Generate draft rows by category using the prompts in the `prompts/` folder.
3. Save draft rows in `drafts/v2_batches/`.
4. Run draft batch validation.
5. Review draft rows for safety, privacy, originality, and category consistency.
6. Fix or remove flagged rows.
7. Merge approved rows into `data/synthetic_child_behavior_notes_v2_1000.csv`.
8. Run full dataset validation.
9. Create a final v2 validation report.

## Review Checks

Each batch should be checked for:

- missing fields
- duplicate IDs
- invalid label values
- privacy issues
- phone numbers, email addresses, dates, or personal details
- diagnosis or treatment wording
- category mismatch
- unsupported consequence fields
- repeated or copied-sounding wording

## Final v2 Release

Before publishing v2, the dataset should include:

- 1,000 rows
- validation report
- README update
- schema documentation
- ethics and limitations documentation
- category documentation
- Hugging Face dataset card
- Kaggle dataset description