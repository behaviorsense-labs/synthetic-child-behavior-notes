"""
review_final_dataset.py

Runs a consolidated static check + one AI review pass on the final merged
dataset. Designed for the full file — ignores known acceptable differences
between v1 and v2 rows, and focuses only on issues that matter for publishing.

Usage:
    python scripts/review_final_dataset.py data/synthetic_child_behavior_notes_v2_final.csv
"""

import os
import sys
from pathlib import Path

import pandas as pd
from openai import OpenAI

OUTPUT_DIR = Path("drafts/v2_batches/reviews")
MODEL = "gpt-4o-mini"

# Only these fields are strictly validated
STRICT_FIELDS = {
    "age_group":          {"3-5", "6-8", "9-12"},
    "risk_level":         {"low", "moderate", "high"},
    "difficulty_level":   {"easy", "medium", "complex"},
    "ambiguity_level":    {"low", "medium", "high"},
    "split":              {"train", "validation", "test"},
    "consequence_present": {"yes", "no"},
}

# Setting vocabulary — v2 only (v1 used freeform, that's acceptable)
V2_SETTINGS = {
    "home", "school-classroom", "school-playground", "public-store",
    "public-restaurant", "public-transport", "outdoor", "daycare",
    "relative-home", "other-public",
}

SIMILARITY_THRESHOLD = 0.6  # only flag very close duplicates


def tokenize(text: str) -> set:
    return set(str(text).lower().split())


def jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    union = len(a | b)
    return len(a & b) / union if union else 0.0


def run_static_check(df: pd.DataFrame) -> str:
    issues = []

    # 1. Strict field validation (both v1 and v2)
    for field, allowed in STRICT_FIELDS.items():
        if field not in df.columns:
            continue
        bad = df[
            (df[field].str.strip() != "") &
            (~df[field].str.lower().isin(allowed))
        ][["id", field]]
        for _, row in bad.iterrows():
            issues.append(f"Row {row['id']} | `{field}` = '{row[field]}' — expected one of {sorted(allowed)}")

    # 2. Setting validation — v2 rows only
    if "setting" in df.columns and "dataset_version" in df.columns:
        v2 = df[df["dataset_version"] == "v2"]
        bad_setting = v2[~v2["setting"].str.lower().isin(V2_SETTINGS)][["id", "setting"]]
        for _, row in bad_setting.iterrows():
            issues.append(f"Row {row['id']} | `setting` = '{row['setting']}' — not in v2 controlled vocabulary")

    # 3. Empty critical fields
    for field in ["observation_text", "behavior", "category"]:
        if field not in df.columns:
            continue
        empty = df[df[field].str.strip() == ""][["id"]]
        for _, row in empty.iterrows():
            issues.append(f"Row {row['id']} | `{field}` is empty")

    # 4. Duplicate IDs
    dupes = df[df["id"].duplicated()]["id"].tolist()
    if dupes:
        issues.append(f"Duplicate IDs found: {dupes}")

    # 5. Category distribution
    if "category" in df.columns:
        counts = df["category"].value_counts()
        for cat, count in counts.items():
            if count < 10:
                issues.append(f"Category '{cat}' has only {count} rows — may be too thin")

    # 6. Near-duplicates — v2 only, high threshold
    if "dataset_version" in df.columns:
        v2 = df[df["dataset_version"] == "v2"].copy()
        rows = v2[["id", "observation_text", "behavior"]].fillna("").to_dict("records")
        dup_issues = []
        for i in range(len(rows)):
            for j in range(i + 1, len(rows)):
                a, b = rows[i], rows[j]
                obs = jaccard(tokenize(a["observation_text"]), tokenize(b["observation_text"]))
                beh = jaccard(tokenize(a["behavior"]), tokenize(b["behavior"]))
                if obs >= SIMILARITY_THRESHOLD and beh >= SIMILARITY_THRESHOLD:
                    dup_issues.append(
                        f"Rows {a['id']} and {b['id']} are very similar "
                        f"(observation={obs:.2f}, behavior={beh:.2f})"
                    )
        issues.extend(dup_issues)

    # Summary
    total = len(df)
    v1_count = len(df[df["dataset_version"] == "v1"]) if "dataset_version" in df.columns else 0
    v2_count = len(df[df["dataset_version"] == "v2"]) if "dataset_version" in df.columns else 0

    lines = [
        f"## Dataset Overview",
        f"",
        f"- Total rows: {total}",
        f"- v1 rows: {v1_count}",
        f"- v2 rows: {v2_count}",
        f"- Categories: {df['category'].nunique() if 'category' in df.columns else 'unknown'}",
        f"",
        f"## Category Distribution",
        f"",
    ]
    if "category" in df.columns:
        for cat, count in df["category"].value_counts().sort_index().items():
            lines.append(f"- {cat}: {count} rows")

    lines += [
        f"",
        f"## Issues Found ({len(issues)} total)",
        f"",
    ]

    if not issues:
        lines.append("No significant issues found.")
    else:
        for issue in issues:
            lines.append(f"- {issue}")

    return "\n".join(lines)


def run_ai_review(client: OpenAI, df: pd.DataFrame) -> str:
    """
    Sample 30 rows across categories and run one AI quality review.
    Cheaper than reviewing all 697 rows, still representative.
    """
    # Sample 2 rows per category
    sampled = (
        df.groupby("category", group_keys=False)
          .apply(lambda g: g.sample(min(5, len(g)), random_state=42))
          .reset_index(drop=True)
    )

    csv_sample = sampled.to_csv(index=False)

    system_prompt = """You are reviewing a sample of rows from a synthetic child behavior dataset.
This is test data for AI research — it is not clinical data.

Review the sample for:
- Any diagnostic or clinical language (e.g. ADHD, autism, disorder names)
- Any rows that sound like real private records rather than synthetic data
- Any rows with obviously wrong category labels
- Any rows with harmful, stigmatizing, or inappropriate content
- Any rows where the behavior field is too vague to be useful

Do NOT flag:
- Minor wording variation
- Freeform setting values (some rows use older format)
- Consequence field wording style
- General quality nitpicks

Be concise. Only flag genuine problems. If the batch looks good, say so."""

    user_message = f"Here is a sample of {len(sampled)} rows from the dataset:\n\n{csv_sample}"

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python scripts/review_final_dataset.py <final_csv_file>")
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
    df = pd.read_csv(csv_file, dtype=str).fillna("")

    # Normalise case on controlled fields
    for field in list(STRICT_FIELDS.keys()) + ["setting", "dataset_version"]:
        if field in df.columns:
            df[field] = df[field].str.strip().str.lower()

    print("Running static checks...")
    static_result = run_static_check(df)

    print("Running AI review on sample...")
    client = OpenAI()
    ai_result = run_ai_review(client, df)

    report = f"""# Final Dataset Review

Source file: `{csv_file}`

---

{static_result}

---

## AI Quality Review (sample of 5 rows per category)

{ai_result}
"""

    output_file = OUTPUT_DIR / f"{csv_file.stem}_final_review.md"
    output_file.write_text(report, encoding="utf-8")
    print(f"\nSaved: {output_file}")


if __name__ == "__main__":
    main()