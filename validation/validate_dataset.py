import csv
from collections import Counter
from pathlib import Path

DATA_FILE = Path("data/synthetic_child_behavior_notes_v1_300.csv")
REPORT_FILE = Path("validation/validation_report_v1.md")

required_columns = [
    "id",
    "dataset_version",
    "observation_text",
    "age_group",
    "setting",
    "antecedent",
    "behavior",
    "consequence",
    "consequence_present",
    "possible_trigger",
    "emotion_context",
    "caregiver_response",
    "suggested_followup_question",
    "general_support_idea",
    "category",
    "risk_level",
    "difficulty_level",
    "ambiguity_level",
    "split",
    "synthetic_flag",
    "review_status",
]

valid_splits = {"train", "validation", "test"}
valid_risk_levels = {"low", "moderate", "high"}
valid_difficulty_levels = {"easy", "medium", "complex"}
valid_ambiguity_levels = {"low", "medium", "high"}
valid_yes_no = {"yes", "no"}

pii_words = ["phone", "email", "@", "address", "street", "ssn", "social security"]

def main():
    errors = []
    rows = []

    if not DATA_FILE.exists():
        print(f"Missing file: {DATA_FILE}")
        return

    with DATA_FILE.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    columns = reader.fieldnames or []

    for col in required_columns:
        if col not in columns:
            errors.append(f"Missing column: {col}")

    ids = [row.get("id", "").strip() for row in rows]
    duplicate_ids = [item for item, count in Counter(ids).items() if count > 1 and item]

    if duplicate_ids:
        errors.append(f"Duplicate IDs found: {duplicate_ids}")

    for row in rows:
        row_id = row.get("id", "unknown")

        for col in required_columns:
            if not row.get(col, "").strip():
                errors.append(f"Row {row_id}: missing value in {col}")

        if row.get("split") not in valid_splits:
            errors.append(f"Row {row_id}: invalid split")

        if row.get("risk_level") not in valid_risk_levels:
            errors.append(f"Row {row_id}: invalid risk_level")

        if row.get("difficulty_level") not in valid_difficulty_levels:
            errors.append(f"Row {row_id}: invalid difficulty_level")

        if row.get("ambiguity_level") not in valid_ambiguity_levels:
            errors.append(f"Row {row_id}: invalid ambiguity_level")

        if row.get("consequence_present") not in valid_yes_no:
            errors.append(f"Row {row_id}: invalid consequence_present")

        if row.get("synthetic_flag") != "yes":
            errors.append(f"Row {row_id}: synthetic_flag should be yes")

        text_to_check = " ".join([
            row.get("observation_text", ""),
            row.get("antecedent", ""),
            row.get("behavior", ""),
            row.get("caregiver_response", ""),
        ]).lower()

        for word in pii_words:
            if word in text_to_check:
                errors.append(f"Row {row_id}: possible privacy issue word found: {word}")

    category_counts = Counter(row.get("category", "") for row in rows)
    split_counts = Counter(row.get("split", "") for row in rows)
    difficulty_counts = Counter(row.get("difficulty_level", "") for row in rows)
    ambiguity_counts = Counter(row.get("ambiguity_level", "") for row in rows)

    report = []
    report.append("# Validation Report - v1\n")
    report.append(f"Total rows checked: {len(rows)}\n")
    report.append(f"Total errors found: {len(errors)}\n")

    report.append("## Category Counts\n")
    for key, value in category_counts.items():
        report.append(f"- {key}: {value}")

    report.append("\n## Split Counts\n")
    for key, value in split_counts.items():
        report.append(f"- {key}: {value}")

    report.append("\n## Difficulty Counts\n")
    for key, value in difficulty_counts.items():
        report.append(f"- {key}: {value}")

    report.append("\n## Ambiguity Counts\n")
    for key, value in ambiguity_counts.items():
        report.append(f"- {key}: {value}")

    report.append("\n## Errors\n")
    if errors:
        for error in errors:
            report.append(f"- {error}")
    else:
        report.append("- No errors found.")

    REPORT_FILE.write_text("\n".join(report), encoding="utf-8")

    print(f"Rows checked: {len(rows)}")
    print(f"Errors found: {len(errors)}")
    print(f"Report saved to: {REPORT_FILE}")

if __name__ == "__main__":
    main()
