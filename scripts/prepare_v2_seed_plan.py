from pathlib import Path
import csv
from collections import Counter

V1_FILE = Path("data/synthetic_child_behavior_notes_v1_300.csv")
PLAN_FILE = Path("docs/v2_expansion_plan.md")

TARGET_TOTAL = 1000

def main():
    with V1_FILE.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    category_counts = Counter(row["category"] for row in rows)

    categories = list(category_counts.keys())
    base_target = TARGET_TOTAL // len(categories)
    remaining = TARGET_TOTAL % len(categories)

    lines = []
    lines.append("# V2 Expansion Plan")
    lines.append("")
    lines.append(f"Current v1 rows: {len(rows)}")
    lines.append(f"Target v2 rows: {TARGET_TOTAL}")
    lines.append("")
    lines.append("## Category Plan")
    lines.append("")
    lines.append("| Category | Current Rows | Target Rows | Rows to Add |")
    lines.append("|---|---:|---:|---:|")

    total_target = 0

    for index, category in enumerate(categories):
        target = base_target + (1 if index < remaining else 0)
        current = category_counts[category]
        to_add = target - current
        total_target += target
        lines.append(f"| {category} | {current} | {target} | {to_add} |")

    lines.append("")
    lines.append(f"Planned total rows: {total_target}")
    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- v2 will expand the dataset from 300 to 1,000 rows.")
    lines.append("- The same schema will be used.")
    lines.append("- New rows should remain synthetic, caregiver-centered, non-clinical, and privacy-safe.")
    lines.append("- v2 should include validation before publishing to Hugging Face or Kaggle.")

    PLAN_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Created {PLAN_FILE}")

if __name__ == "__main__":
    main()
