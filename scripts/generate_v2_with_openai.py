import csv
import io
import os
from pathlib import Path

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_FILE = Path("prompts/01_generate_rows.md")
OUTPUT_DIR = Path("drafts/v2_batches")

# Columns the model is asked to generate (18 fields).
# dataset_version, synthetic_flag, and review_status are always fixed —
# the script injects them after parsing so the model never outputs them.
MODEL_COLUMNS = [
    "id", "observation_text", "age_group", "setting",
    "antecedent", "behavior", "consequence", "consequence_present",
    "possible_trigger", "emotion_context", "caregiver_response",
    "suggested_followup_question", "general_support_idea", "category",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
]

# Full schema written to the output CSV (21 fields).
EXPECTED_COLUMNS = [
    "id", "dataset_version", "observation_text", "age_group", "setting",
    "antecedent", "behavior", "consequence", "consequence_present",
    "possible_trigger", "emotion_context", "caregiver_response",
    "suggested_followup_question", "general_support_idea", "category",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
    "synthetic_flag", "review_status",
]

# Index of the last free-text field before the controlled-vocabulary tail.
# Uses MODEL_COLUMNS (19 fields) since that's what the model outputs.
TAIL_START = MODEL_COLUMNS.index("category")   # = 13
TAIL_COLUMNS = MODEL_COLUMNS[TAIL_START:]       # 6 fixed fields at the end

# Fields whose values must be lowercased
LOWERCASE_FIELDS = {
    "dataset_version", "age_group", "setting", "consequence_present",
    "risk_level", "difficulty_level", "ambiguity_level", "split",
    "synthetic_flag", "review_status",
}

# Fixed values that must always be set regardless of what the model wrote
FIXED_VALUES = {
    "dataset_version": "v2",
    "synthetic_flag": "yes",
    "review_status": "draft",
}

# Split large batches into chunks of MAX_ROWS_PER_CALL to avoid truncation.
MAX_ROWS_PER_CALL = 20

# -------------------------------------------------------------------
# BATCHES — one entry per category.
# screen-time ending (rows 301–347, 47 rows) was generated separately
# and is kept as-is. The remaining 14 categories start from row 348.
# Each batch generates 25 rows. Run the script, then update BATCHES
# to the next category before running again, or run all at once.
# -------------------------------------------------------------------
BATCHES = [
    # already done — kept for reference, do not re-run
    # {"category": "screen-time ending", "rows": 47, "start_id": 301, "end_id": 347, "output_file": "screen_time_ending_rows_301_347.csv"},

    {"category": "transition difficulty",      "rows": 25, "start_id": 348, "end_id": 372, "output_file": "transition_difficulty_rows_348_372.csv"},
    {"category": "homework frustration",        "rows": 25, "start_id": 373, "end_id": 397, "output_file": "homework_frustration_rows_373_397.csv"},
    {"category": "bedtime resistance",          "rows": 25, "start_id": 398, "end_id": 422, "output_file": "bedtime_resistance_rows_398_422.csv"},
    {"category": "mealtime refusal",            "rows": 25, "start_id": 423, "end_id": 447, "output_file": "mealtime_refusal_rows_423_447.csv"},
    {"category": "sensory overload",            "rows": 25, "start_id": 448, "end_id": 472, "output_file": "sensory_overload_rows_448_472.csv"},
    {"category": "communication frustration",   "rows": 25, "start_id": 473, "end_id": 497, "output_file": "communication_frustration_rows_473_497.csv"},
    {"category": "social conflict",             "rows": 25, "start_id": 498, "end_id": 522, "output_file": "social_conflict_rows_498_522.csv"},
    {"category": "classroom attention",         "rows": 25, "start_id": 523, "end_id": 547, "output_file": "classroom_attention_rows_523_547.csv"},
    {"category": "waiting / turn-taking",       "rows": 25, "start_id": 548, "end_id": 572, "output_file": "waiting_turn_taking_rows_548_572.csv"},
    {"category": "cleanup difficulty",          "rows": 25, "start_id": 573, "end_id": 597, "output_file": "cleanup_difficulty_rows_573_597.csv"},
    {"category": "morning routine",             "rows": 25, "start_id": 598, "end_id": 622, "output_file": "morning_routine_rows_598_622.csv"},
    {"category": "public place overload",       "rows": 25, "start_id": 623, "end_id": 647, "output_file": "public_place_overload_rows_623_647.csv"},
    {"category": "separation anxiety",          "rows": 25, "start_id": 648, "end_id": 672, "output_file": "separation_anxiety_rows_648_672.csv"},
    {"category": "routine change",              "rows": 25, "start_id": 673, "end_id": 697, "output_file": "routine_change_rows_673_697.csv"},
]


def build_prompt(batch: dict) -> str:
    prompt = PROMPT_FILE.read_text(encoding="utf-8")
    prompt = prompt.replace("CATEGORY_NAME_HERE", batch["category"])
    prompt = prompt.replace("NUMBER_OF_ROWS_HERE", str(batch["rows"]))
    prompt = prompt.replace(
        "START_ID_HERE to END_ID_HERE",
        f'{batch["start_id"]} to {batch["end_id"]}',
    )
    return prompt


def repair_row(raw_fields: list[str]) -> dict | None:
    """
    Attempt to repair a column-shifted row.

    When the model writes an unquoted comma inside a free-text field,
    every column after it shifts right by one. Since the tail columns
    (category onward) are short controlled values, we can identify the
    tail by scanning from the right and reconstruct the free-text field
    that was split.

    Returns a repaired dict, or None if repair is not possible.
    """
    expected = len(MODEL_COLUMNS)
    actual = len(raw_fields)

    if actual <= expected:
        return None  # not a column-shift problem

    # The tail fields (category onward) are always short single values.
    # Pull them off the right side first.
    tail_values = raw_fields[actual - len(TAIL_COLUMNS):]
    head_values = raw_fields[: actual - len(TAIL_COLUMNS)]

    head_columns = MODEL_COLUMNS[:TAIL_START]

    if len(head_values) < len(head_columns):
        return None  # too few fields even after split — can't repair

    # Merge the extra values back into the last free-text head field
    repaired_head = list(head_values[: len(head_columns) - 1])
    merged_last = ", ".join(head_values[len(head_columns) - 1:])
    repaired_head.append(merged_last)

    all_values = repaired_head + tail_values
    if len(all_values) != expected:
        return None  # repair didn't produce the right count

    return dict(zip(MODEL_COLUMNS, all_values))


def clean_rows(raw_text: str) -> tuple[list[dict], list[str]]:
    """
    Parse and clean generated CSV rows.
    Returns (clean_rows, skipped_row_warnings).

    Handles:
    - Trailing whitespace on all fields
    - Wrong case on controlled-vocabulary fields
    - Fixed values (dataset_version, synthetic_flag, review_status)
    - Column-shifted rows: attempts repair before skipping
    - Header rows accidentally included by the model
    """
    clean = []
    skipped = []

    lines = io.StringIO(raw_text)
    header_line = None
    data_lines = []

    # Split into header and data lines
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        if header_line is None:
            # First non-blank line — check if it looks like a header
            first_field = next(csv.reader([stripped]))[0].strip().lower()
            if first_field == "id":
                header_line = stripped
            else:
                # No header — model went straight to data, use MODEL_COLUMNS
                data_lines.append(stripped)
        else:
            data_lines.append(stripped)

    # Determine actual columns from header if present, else fall back to MODEL_COLUMNS
    if header_line:
        actual_columns = [c.strip() for c in next(csv.reader([header_line]))]
    else:
        actual_columns = MODEL_COLUMNS

    for i, line in enumerate(data_lines, start=1):
        raw_fields = [f.strip() for f in next(csv.reader([line]))]

        if not raw_fields or raw_fields == [""]:
            continue

        if len(raw_fields) > len(actual_columns):
            # Too many fields — unquoted comma in free-text, attempt repair
            repaired = repair_row(raw_fields)
            if repaired:
                row = repaired
            else:
                # Repair failed — truncate to expected column count
                row = dict(zip(actual_columns, raw_fields[:len(actual_columns)]))
        else:
            # Fewer or equal fields — map what we have, fill rest with empty string
            # Missing fields will be caught and reported by the static validator
            row = dict(zip(actual_columns, raw_fields))
            for col in actual_columns:
                row.setdefault(col, "")

        # Strip whitespace from all values
        row = {k: v.strip() for k, v in row.items()}

        # Lowercase controlled-vocabulary fields
        for field in LOWERCASE_FIELDS:
            if field in row:
                row[field] = row[field].lower()

        # Inject fixed columns not generated by the model
        row["dataset_version"] = "v2"
        row["synthetic_flag"] = "yes"
        row["review_status"] = "draft"

        # Enforce any remaining fixed values
        for field, value in FIXED_VALUES.items():
            row[field] = value

        # Reorder to match full EXPECTED_COLUMNS output schema
        row = {col: row.get(col, "") for col in EXPECTED_COLUMNS}

        clean.append(row)

    return clean, skipped


def main() -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for batch in BATCHES:
        total_rows = batch["rows"]
        start_id = batch["start_id"]
        print(f"Generating: {batch['category']} ({total_rows} rows in chunks of {MAX_ROWS_PER_CALL})")

        all_clean = []
        all_skipped = []
        current_id = start_id

        while current_id <= batch["end_id"]:
            chunk_size = min(MAX_ROWS_PER_CALL, batch["end_id"] - current_id + 1)
            chunk_end = current_id + chunk_size - 1

            print(f"  Chunk: rows {current_id}–{chunk_end} ({chunk_size} rows)...")

            chunk_batch = {
                **batch,
                "rows": chunk_size,
                "start_id": current_id,
                "end_id": chunk_end,
            }
            prompt = build_prompt(chunk_batch)

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.8,
            )

            raw_text = response.choices[0].message.content.strip()
            clean, skipped = clean_rows(raw_text)
            all_clean.extend(clean)
            all_skipped.extend(skipped)

            print(f"    Got {len(clean)} clean rows, {len(skipped)} skipped.")
            current_id = chunk_end + 1

        if all_skipped:
            print(f"\n  Skipped {len(all_skipped)} malformed row(s) total:")
            for w in all_skipped:
                print(f"    - {w}")

        output_path = OUTPUT_DIR / batch["output_file"]

        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_COLUMNS, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            writer.writerows(all_clean)

        print(f"Saved: {output_path} ({len(all_clean)} rows total)")

        if all_skipped:
            print(f"  Note: {len(all_skipped)} row(s) skipped — regenerate to fill gaps.")


if __name__ == "__main__":
    main()