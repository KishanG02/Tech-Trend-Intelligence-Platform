import json
from pathlib import Path
from collections import Counter

PROCESSED_PATH = Path(
    "data-lake/processed/news"
)

ANALYTICS_PATH = Path(
    "data-lake/analytics"
)

ANALYTICS_PATH.mkdir(
    parents=True,
    exist_ok=True
)

keyword_counter = Counter()

for file in PROCESSED_PATH.glob("*.json"):

    with open(file, "r") as f:

        data = json.load(f)

        keyword = data.get("keyword")

        if keyword:
            keyword_counter[keyword] += 1

summary = {
    "total_articles": sum(
        keyword_counter.values()
    ),
    "articles_per_keyword":
        dict(keyword_counter)
}

output_file = (
    ANALYTICS_PATH /
    "keyword_summary.json"
)

with open(output_file, "w") as f:
    json.dump(
        summary,
        f,
        indent=4
    )

print(
    json.dumps(
        summary,
        indent=4
    )
)