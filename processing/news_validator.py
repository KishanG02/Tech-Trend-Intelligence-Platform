import json
import shutil
from pathlib import Path

RAW_PATH = Path("data-lake/raw/news")
PROCESSED_PATH = Path("data-lake/processed/news")
LOG_PATH = Path("data-lake/logs")

PROCESSED_PATH.mkdir(parents=True, exist_ok=True)
LOG_PATH.mkdir(parents=True, exist_ok=True)

seen_urls = set()

valid_count = 0
invalid_count = 0

for file in RAW_PATH.glob("*.json"):

    try:
        with open(file, "r") as f:
            data = json.load(f)

        title = data.get("title")
        description = data.get("description")
        url = data.get("url")

        valid = True

        if not title:
            valid = False

        if not description:
            valid = False

        if not url:
            valid = False

        if url in seen_urls:
            valid = False

        if valid:

            seen_urls.add(url)

            shutil.copy(
                file,
                PROCESSED_PATH / file.name
            )

            valid_count += 1

            print(f"VALID   : {file.name}")

        else:

            invalid_count += 1

            print(f"INVALID : {file.name}")

    except Exception as e:

        invalid_count += 1

        print(f"ERROR    : {file.name}")
        print(e)

print("\nSummary")
print("-" * 40)
print(f"Valid Records   : {valid_count}")
print(f"Invalid Records : {invalid_count}")