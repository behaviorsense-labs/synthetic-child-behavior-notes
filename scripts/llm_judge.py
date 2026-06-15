"""
llm_judge.py

Runs 3 LLM-as-Judge evaluations on the final dataset and outputs
markdown tables ready to paste into Excel for visualization.

Usage:
    python scripts/llm_judge.py data/synthetic_child_behavior_notes_v2_final.csv

Output files in drafts/judge_results/:
    judge_01_quality_results.md
    judge_02_diversity_results.md
    judge_03_usefulness_results.md
"""

import os
import sys
from pathlib import Path

import pandas as pd
from openai import OpenAI

OUTPUT_DIR = Path("drafts/judge_results")
MODEL = "gpt-4o-mini"

PROMPTS = [
    {
        "name": "quality",
        "file": Path("prompts/judge_01_quality.md"),
        "title": "Judge 1 — Quality Scores",
        "batch_size": 20,       # rows per API call
        "group_by": None,       # no grouping needed
    },
    {
        "name": "diversity",
        "file": Path("prompts/judge_02_diversity.md"),
        "title": "Judge 2 — Diversity Scores",
        "batch_size": None,     # send whole category at once
        "group_by": "category", # score within each category
    },
    {
        "name": "usefulness",
        "file": Path("prompts/judge_03_usefulness.md"),
        "title": "Judge 3 — Usefulness Scores",
        "batch_size": 20,
        "group_by": None,
    },
]


def build_row_text(row: pd.Series) -> str:
    """Format a single row as readable text for the LLM."""
    return (
        f"row_id: {row.get('id', '')}\n"
        f"category: {row.get('category', '')}\n"
        f"age_group: {row.get('age_group', '')}\n"
        f"setting: {row.get('setting', '')}\n"
        f"observation_text: {row.get('observation_text', '')}\n"
        f"antecedent: {row.get('antecedent', '')}\n"
        f"behavior: {row.get('behavior', '')}\n"
        f"consequence: {row.get('consequence', '')}\n"
        f"consequence_present: {row.get('consequence_present', '')}\n"
        f"possible_trigger: {row.get('possible_trigger', '')}\n"
        f"emotion_context: {row.get('emotion_context', '')}\n"
        f"caregiver_response: {row.get('caregiver_response', '')}\n"
        f"general_support_idea: {row.get('general_support_idea', '')}\n"
    )


def call_judge(client: OpenAI, system_prompt: str, rows_text: str) -> str:
    """Call the LLM judge and return the raw markdown table response."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Evaluate these rows:\n\n{rows_text}"},
        ],
        temperature=0.1,  # low temperature for consistent scoring
    )
    return response.choices[0].message.content.strip()


def run_quality_or_usefulness(
    client: OpenAI,
    df: pd.DataFrame,
    prompt_text: str,
    batch_size: int,
    title: str,
) -> str:
    """Run quality or usefulness judge in batches across all rows."""
    all_results = []
    total = len(df)

    for start in range(0, total, batch_size):
        batch = df.iloc[start:start + batch_size]
        rows_text = "\n---\n".join(build_row_text(row) for _, row in batch.iterrows())

        end = min(start + batch_size, total)
        print(f"  Rows {start + 1}–{end} of {total}...")

        result = call_judge(client, prompt_text, rows_text)

        # Strip header row from subsequent batches to avoid duplicates
        lines = result.strip().split("\n")
        if all_results and lines:
            # Skip header and separator lines (first 2 lines)
            lines = [l for l in lines if not l.startswith("| row_id") and not l.startswith("|---") and not l.startswith("|------")]
        all_results.extend(lines)

    return f"# {title}\n\n" + "\n".join(all_results)


def run_diversity(
    client: OpenAI,
    df: pd.DataFrame,
    prompt_text: str,
    title: str,
) -> str:
    """Run diversity judge per category."""
    all_results = []
    df.columns = df.columns.str.strip()  # ensure clean column names
    categories = sorted(df["category"].unique())

    for cat in categories:
        cat_df = df[df["category"] == cat]
        rows_text = "\n---\n".join(build_row_text(row) for _, row in cat_df.iterrows())

        print(f"  Category: {cat} ({len(cat_df)} rows)...")

        result = call_judge(client, prompt_text, rows_text)

        lines = result.strip().split("\n")
        if all_results:
            lines = [l for l in lines if not l.startswith("| row_id") and not l.startswith("|---") and not l.startswith("|------")]
        all_results.extend(lines)

    return f"# {title}\n\n" + "\n".join(all_results)


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/llm_judge.py <final_csv_file>")
        raise SystemExit(1)

    csv_file = Path(sys.argv[1])
    if not csv_file.exists():
        print(f"File not found: {csv_file}")
        raise SystemExit(1)

    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY is not set.")
        raise SystemExit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Loading dataset...")
    df = pd.read_csv(csv_file, dtype=str, encoding="utf-8-sig").fillna("")
    df.columns = df.columns.str.strip()  # remove any leading/trailing spaces from column names
    print(f"Loaded {len(df)} rows across {df['category'].nunique()} categories.")

    # Sample 20 rows per category for evaluation
    SAMPLE_PER_CATEGORY = 20
    # Sample per category without losing the category column
    sampled_frames = []
    for cat, group in df.groupby("category"):
        sampled_frames.append(group.sample(min(SAMPLE_PER_CATEGORY, len(group)), random_state=42))
    df = pd.concat(sampled_frames, ignore_index=True)
    print(f"Sampled {len(df)} rows ({SAMPLE_PER_CATEGORY} per category) for judge evaluation.")

    client = OpenAI()

    sampled_df = df.copy()

    for judge in PROMPTS:
        print(f"\nRunning {judge['title']}...")

        output_file = OUTPUT_DIR / f"judge_{judge['name']}_results.md"
        if output_file.exists():
            print(f"  Already exists, skipping: {output_file}")
            continue

        prompt_text = judge["file"].read_text(encoding="utf-8")

        if judge["group_by"] == "category":
            result = run_diversity(client, sampled_df, prompt_text, judge["title"])
        else:
            result = run_quality_or_usefulness(
                client, sampled_df, prompt_text,
                batch_size=judge["batch_size"],
                title=judge["title"],
            )

        output_file.write_text(result, encoding="utf-8")
        print(f"  Saved: {output_file}")

    print("\nAll judge evaluations complete.")
    print(f"Results in: {OUTPUT_DIR}/")
    print("\nNext step: paste the markdown tables into Excel and build charts.")


if __name__ == "__main__":
    main()