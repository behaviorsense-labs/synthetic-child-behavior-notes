import os
import sys
from pathlib import Path

import pandas as pd
from openai import OpenAI


PROMPTS = [
    {
        "name": "quality_review",
        "prompt_file": Path("prompts/02_review_rows.md"),
        "title": "Quality and Schema Review",
    },
    {
        "name": "originality_review",
        "prompt_file": Path("prompts/03_originality_check.md"),
        "title": "Originality and Similarity Review",
    },
]

OUTPUT_DIR = Path("drafts/v2_batches/reviews")
MODEL = "gpt-4o-mini"

# Allowed values per field — any value outside these is flagged
ALLOWED_VALUES = {
    "dataset_version": {"v2"},
    "age_group": {"3-5", "6-8", "9-12"},
    "setting": {
        "home", "school-classroom", "school-playground", "public-store",
        "public-restaurant", "public-transport", "outdoor", "daycare",
        "relative-home", "other-public",
    },
    "consequence_present": {"yes", "no"},
    "risk_level": {"low", "moderate", "high"},
    "difficulty_level": {"easy", "medium", "complex"},
    "ambiguity_level": {"low", "medium", "high"},
    "split": {"train", "validation", "test"},
    "synthetic_flag": {"yes"},
    "review_status": {"draft"},
}

# Target distribution ranges (min%, max%) per field value
DISTRIBUTION_TARGETS = {
    "age_group": {"3-5": (15, 35), "6-8": (30, 50), "9-12": (25, 45)},
    "risk_level": {"low": (50, 75), "moderate": (20, 40), "high": (5, 15)},
    "difficulty_level": {"easy": (15, 35), "medium": (40, 60), "complex": (15, 35)},
    "ambiguity_level": {"low": (30, 50), "medium": (30, 50), "high": (10, 30)},
    "consequence_present": {"yes": (20, 40), "no": (60, 80)},
}

# Similarity threshold: flag pairs with Jaccard similarity above this
SIMILARITY_THRESHOLD = 0.5


def tokenize(text: str) -> set:
    """Simple word tokenizer for Jaccard similarity."""
    return set(str(text).lower().split())


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    intersection = len(a & b)
    union = len(a | b)
    return intersection / union if union else 0.0


def run_schema_check(df: pd.DataFrame) -> list[str]:
    """Check all field values are within allowed vocabulary."""
    issues = []
    for field, allowed in ALLOWED_VALUES.items():
        if field not in df.columns:
            issues.append(f"MISSING COLUMN: `{field}` not found in CSV.")
            continue
        bad = df[~df[field].isin(allowed)][["id", field]]
        for _, row in bad.iterrows():
            issues.append(
                f"Row {row['id']} | `{field}` = '{row[field]}' "
                f"— not in allowed values: {sorted(allowed)}"
            )
    return issues


def run_consequence_check(df: pd.DataFrame) -> list[str]:
    """Flag rows where consequence_present=yes but consequence text is vague."""
    vague_phrases = {
        "did not describe", "not described", "not clearly", "no consequence", "no consequence noted",
        "none", "n/a", "", "not mentioned", "calmed after a short", "cried", "concerned about", "left the", "kicked", "ignored", "settled down", "moved to",
    }
    issues = []
    for _, row in df[df["consequence_present"] == "yes"].iterrows():
        consequence = str(row.get("consequence", "")).strip().lower()
        if any(phrase in consequence for phrase in vague_phrases) or len(consequence) < 10:
            issues.append(
                f"Row {row['id']} | consequence_present=yes but consequence "
                f"is vague or empty: '{row['consequence']}'"
            )
    return issues


def run_distribution_check(df: pd.DataFrame) -> list[str]:
    """Flag fields where actual distribution is outside target range."""
    issues = []
    total = len(df)
    if total == 0:
        return ["CSV has no rows."]
    for field, targets in DISTRIBUTION_TARGETS.items():
        if field not in df.columns:
            continue
        counts = df[field].value_counts()
        for value, (min_pct, max_pct) in targets.items():
            actual_count = counts.get(value, 0)
            actual_pct = round(actual_count / total * 100, 1)
            if actual_pct < min_pct:
                issues.append(
                    f"`{field}={value}` is {actual_pct}% ({actual_count} rows) "
                    f"— below target minimum of {min_pct}%"
                )
            elif actual_pct > max_pct:
                issues.append(
                    f"`{field}={value}` is {actual_pct}% ({actual_count} rows) "
                    f"— above target maximum of {max_pct}%"
                )
    return issues


def run_similarity_check(df: pd.DataFrame) -> list[str]:
    """Flag pairs of rows with suspiciously similar behavior + observation text."""
    issues = []
    rows = df[["id", "observation_text", "behavior"]].fillna("").to_dict("records")

    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]

            obs_sim = jaccard(tokenize(a["observation_text"]), tokenize(b["observation_text"]))
            beh_sim = jaccard(tokenize(a["behavior"]), tokenize(b["behavior"]))
            combined = (obs_sim + beh_sim) / 2

            if combined >= SIMILARITY_THRESHOLD:
                issues.append(
                    f"Rows {a['id']} and {b['id']} are similar "
                    f"(observation={obs_sim:.2f}, behavior={beh_sim:.2f}) "
                    f"— consider rewriting one."
                )
    return issues


def run_static_checks(csv_file: Path) -> Path:
    """Run all local checks and save a report."""
    try:
        df = pd.read_csv(csv_file, dtype=str, quoting=0, on_bad_lines="warn").fillna("")
    except Exception as e:
        raise ValueError(
            f"Could not parse CSV: {e}\n"
            "Tip: check that all fields with commas are wrapped in double quotes."
        )

    schema_issues = run_schema_check(df)
    consequence_issues = run_consequence_check(df)
    distribution_issues = run_distribution_check(df)
    similarity_issues = run_similarity_check(df)

    def section(title: str, items: list[str]) -> str:
        if not items:
            return f"## {title}\n\nNo issues found.\n"
        return "## {}\n\n{}\n".format(title, "\n".join(f"- {i}" for i in items))

    report = f"""# Static Validation Report

Source file: `{csv_file}`

Total rows: {len(df)}

{section("Schema Compliance", schema_issues)}
{section("Consequence Field Check", consequence_issues)}
{section("Distribution Check", distribution_issues)}
{section("Near-Duplicate Check", similarity_issues)}
"""

    output_file = OUTPUT_DIR / f"{csv_file.stem}_static_checks.md"
    output_file.write_text(report, encoding="utf-8")
    print(f"Saved: {output_file}")

    total_issues = (
        len(schema_issues)
        + len(consequence_issues)
        + len(distribution_issues)
        + len(similarity_issues)
    )
    print(f"Static check complete — {total_issues} issue(s) found.")
    return output_file


def run_review(
    client: OpenAI,
    csv_file: Path,
    prompt_file: Path,
    title: str,
    review_name: str,
) -> Path:
    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    prompt_text = prompt_file.read_text(encoding="utf-8")
    csv_content = csv_file.read_text(encoding="utf-8")

    system_prompt = prompt_text.strip()
    user_message = f"## Dataset Rows to Review\n\n{csv_content}".strip()

    print(f"Running {title}...")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    review_text = response.choices[0].message.content.strip()

    output_file = OUTPUT_DIR / f"{csv_file.stem}_{review_name}.md"

    report = f"""# {title}

Source file: `{csv_file}`

Prompt used: `{prompt_file}`

Model used: `{MODEL}`

## Review Result

{review_text}
"""

    output_file.write_text(report, encoding="utf-8")
    print(f"Saved: {output_file}")
    return output_file


def review_batch(csv_file: Path) -> list[Path]:
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_file}")

    if csv_file.suffix.lower() != ".csv":
        raise ValueError("Input file must be a CSV file.")

    if csv_file.stat().st_size == 0:
        raise ValueError("Input CSV file is empty.")

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: fast local checks — no API calls, no cost
    print("Running static checks...")
    static_report = run_static_checks(csv_file)

    # Step 2: AI-powered reviews
    client = OpenAI()
    output_files = [static_report]

    for review in PROMPTS:
        output_file = run_review(
            client=client,
            csv_file=csv_file,
            prompt_file=review["prompt_file"],
            title=review["title"],
            review_name=review["name"],
        )
        output_files.append(output_file)

    return output_files


def main() -> None:
    if len(sys.argv) != 2:
        print(
            "Usage: python scripts/review_v2_batch_with_openai.py "
            "<draft_csv_file>"
        )
        raise SystemExit(1)

    csv_file = Path(sys.argv[1])

    try:
        output_files = review_batch(csv_file)

        print("\nReviews completed successfully.")
        for output_file in output_files:
            print(f"- {output_file}")

    except Exception as error:
        print(f"\nError: {error}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()