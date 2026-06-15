# LLM Judge — Usefulness Scoring

You are evaluating rows from a synthetic child behavior observation dataset.
This dataset is designed for caregiver-support AI research and educational prototyping.

## Your Task

For each row, assess whether it would be useful for training or evaluating a caregiver-support AI system.

### Scoring Dimension

**Usefulness** — Would this row help a caregiver-support AI learn to recognize, interpret, or respond to child behavior?

Answer: yes or no

**Confidence** — How confident are you in your usefulness judgment?
- 1 = Not confident
- 3 = Moderately confident
- 5 = Very confident

**Usefulness Reason** — Pick the single best reason:
- good_example = clear, realistic, useful training example
- too_vague = behavior or observation is too vague to be useful
- too_simple = scenario is too simple to add training value
- too_similar = too similar to other common examples
- missing_context = key context fields are missing or empty

## Output Format

Return a markdown table with exactly these columns:

| row_id | category | useful | confidence | usefulness_reason |
|--------|----------|--------|------------|-------------------|

- useful = yes or no only
- Do not include any text before or after the table
- Do not explain your scores
