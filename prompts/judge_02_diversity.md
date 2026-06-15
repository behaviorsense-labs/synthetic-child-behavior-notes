# LLM Judge — Diversity Scoring

You are evaluating rows from a synthetic child behavior observation dataset.
This dataset is designed for caregiver-support AI research. It is not clinical data.

## Your Task

You will receive a batch of rows all from the same category.
Score each row on how distinct it is from the other rows in the batch.

### Scoring Dimension

**Diversity Score** — How different is this row from the other rows in the same category batch?
- 1 = Nearly identical to another row (same setting, same behavior, same trigger)
- 2 = Very similar to at least one other row
- 3 = Some overlap but meaningfully different scenario
- 4 = Clearly distinct scenario
- 5 = Unique scenario, setting, and behavior not seen in other rows

Consider: setting, age group, behavior description, trigger, and caregiver response.

## Output Format

Return a markdown table with exactly these columns:

| row_id | category | age_group | setting | diversity_score | notes |
|--------|----------|-----------|---------|-----------------|-------|

- notes = one short phrase only if two rows are near-identical, otherwise leave blank
- Do not include any text before or after the table
- Do not explain your scores
