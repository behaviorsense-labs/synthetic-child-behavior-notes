"""
merge_final_dataset.py

Combines the v1 dataset (300 rows) and all v2 batch CSVs into a single
final dataset file ready for HuggingFace / Kaggle.

Usage:
    python scripts/merge_final_dataset.py

Output:
    data/synthetic_child_behavior_notes_v2_final.csv
"""

import csv
import sys
from pathlib import Path

import pandas as pd

# ── Paths ────────────────────────────────────────────────────────────────────
V1_FILE = Path("data/synthetic_child_behavior_notes_v1_300.csv")
V2_BATCHES_DIR = Path("drafts/v2_batches")
OUTPUT_FILE = Path("data/synthetic_child_behavior_notes_v2_final.csv")

# ── Expected final schema (21 columns) ───────────────────────────────────────
EXPECTED_COLUMNS = [
    "id", "dataset_version", "observation_text", "age_group", "setting",
    "antecedent", "behavior", "consequence", "consequence_present",
    "possible_trigger", "emotion_context", "caregiver_response",
    "suggested_followup_question", "general_support_idea", "category",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
    "synthetic_flag", "review_status",
]

# Fixed values always injected regardless of source
FIXED_VALUES = {
    "synthetic_flag": "yes",
    "review_status": "draft",
}

# Fields to lowercase for consistency
LOWERCASE_FIELDS = {
    "dataset_version", "age_group", "setting", "consequence_present",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
    "synthetic_flag", "review_status",
}


def load_and_normalise(path: Path, version: str) -> pd.DataFrame:
    """Load a CSV, normalise values, inject fixed fields, return DataFrame."""
    df = pd.read_csv(path, dtype=str).fillna("")

    # Lowercase controlled-vocabulary fields
    for field in LOWERCASE_FIELDS:
        if field in df.columns:
            df[field] = df[field].str.strip().str.lower()

    # Enforce fixed values
    for field, value in FIXED_VALUES.items():
        df[field] = value

    # Set dataset_version
    df["dataset_version"] = version

    # Add any missing columns as empty string
    for col in EXPECTED_COLUMNS:
        if col not in df.columns:
            df[col] = ""

    # Reorder to final schema
    df = df[EXPECTED_COLUMNS]

    return df


def main() -> None:
    frames = []

    # ── Load v1 ──────────────────────────────────────────────────────────────
    if not V1_FILE.exists():
        print(f"WARNING: v1 file not found at {V1_FILE} — skipping.")
    else:
        df_v1 = load_and_normalise(V1_FILE, version="v1")
        frames.append(df_v1)
        print(f"Loaded v1: {len(df_v1)} rows from {V1_FILE}")

    # ── Load v2 batches ───────────────────────────────────────────────────────
    v2_files = sorted(V2_BATCHES_DIR.glob("*.csv"))
    if not v2_files:
        print(f"WARNING: No v2 batch CSVs found in {V2_BATCHES_DIR}")
    else:
        for f in v2_files:
            df_batch = load_and_normalise(f, version="v2")
            frames.append(df_batch)
            print(f"Loaded v2 batch: {len(df_batch)} rows from {f.name}")

    if not frames:
        print("No data loaded. Exiting.")
        sys.exit(1)

    # ── Merge ─────────────────────────────────────────────────────────────────
    final = pd.concat(frames, ignore_index=True)

    # ── Sanity checks ─────────────────────────────────────────────────────────
    print(f"\n── Merge summary ──────────────────────────────────────────")
    print(f"Total rows:     {len(final)}")
    print(f"Total columns:  {len(final.columns)}")
    print(f"\nRows per category:")
    print(final["category"].value_counts().sort_index().to_string())
    print(f"\nRows per dataset_version:")
    print(final["dataset_version"].value_counts().to_string())
    print(f"\nDuplicate IDs: {final['id'].duplicated().sum()}")
    print(f"Empty observation_text: {(final['observation_text'].str.strip() == '').sum()}")

    # ── Save ──────────────────────────────────────────────────────────────────
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    final.to_csv(OUTPUT_FILE, index=False, quoting=csv.QUOTE_ALL)
    print(f"\nSaved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()