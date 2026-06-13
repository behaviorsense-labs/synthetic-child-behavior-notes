import csv
import re
import sys
from collections import Counter
from pathlib import Path

required_columns = [
    "id", "dataset_version", "observation_text", "age_group", "setting",
    "antecedent", "behavior", "consequence", "consequence_present",
    "possible_trigger", "emotion_context", "caregiver_response",
    "suggested_followup_question", "general_support_idea", "category",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
    "synthetic_flag", "review_status"
]

valid_splits = {"train", "validation", "test"}
valid_risk_levels = {"low", "moderate", "high"}
valid_difficulty_levels = {"easy", "medium", "complex"}
valid_ambiguity_levels = {"low", "medium", "high"}
valid_yes_no = {"yes", "no"}

privacy_words = [
    "email", "address",  "ssn", "social security",
    "date of birth", "dob", "full name", "school name", "clinic name"
]

email_pattern = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
phone_pattern = re.compile(r"(\+?\d[\d\s\-\(\)]{7,}\d)")
date_pattern = re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b")

def validate_file(file_path):
    errors = []

    path = Path(file_path)
    if not path.exists():
        print(f"File not found: {path}")
        return

    with path.open("r", encoding="utf-8", newline="") as f:
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

        if row.get("dataset_version") != "v2":
            errors.append(f"Row {row_id}: dataset_version should be v2")

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

        text = " ".join(row.get(col, "") for col in required_columns).lower()

        if email_pattern.search(text):
            errors.append(f"Row {row_id}: possible email found")

        if phone_pattern.search(text):
            errors.append(f"Row {row_id}: possible phone number found")

        if date_pattern.search(text):
            errors.append(f"Row {row_id}: possible date found")

        for word in privacy_words:
            if word in text:
                errors.append(f"Row {row_id}: possible privacy word found: {word}")

    print(f"File checked: {path}")
    print(f"Rows checked: {len(rows)}")
    print(f"Errors found: {len(errors)}")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")
    else:
        print("No errors found.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validation/validate_draft_batch.py <csv_file>")
    else:
        validate_file(sys.argv[1])