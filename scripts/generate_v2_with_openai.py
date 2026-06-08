import os
from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

PROMPT_FILE = Path("prompts/01_generate_rows.md")
OUTPUT_DIR = Path("drafts/v2_batches")

BATCHES = [
    {
        "category": "screen-time ending",
        "rows": 47,
        "start_id": 301,
        "end_id": 347,
        "output_file": "screen_time_ending_rows_301_347.csv",
    }
]

def build_prompt(batch):
    prompt = PROMPT_FILE.read_text(encoding="utf-8")

    prompt = prompt.replace("CATEGORY_NAME_HERE", batch["category"])
    prompt = prompt.replace("NUMBER_OF_ROWS_HERE", str(batch["rows"]))
    prompt = prompt.replace(
        "START_ID_HERE to END_ID_HERE",
        f'{batch["start_id"]} to {batch["end_id"]}'
    )

    return prompt

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for batch in BATCHES:
        print(f"Generating: {batch['category']}")

        prompt = build_prompt(batch)

        response = client.responses.create(
            model="gpt-5.5",
            input=prompt,
        )

        output_text = response.output_text.strip()

        output_path = OUTPUT_DIR / batch["output_file"]

        header = (
            "id,dataset_version,observation_text,age_group,setting,"
            "antecedent,behavior,consequence,consequence_present,"
            "possible_trigger,emotion_context,caregiver_response,"
            "suggested_followup_question,general_support_idea,category,"
            "risk_level,difficulty_level,ambiguity_level,split,"
            "synthetic_flag,review_status\n"
        )

        output_path.write_text(header + output_text + "\n", encoding="utf-8")

        print(f"Saved: {output_path}")

if __name__ == "__main__":
    main()