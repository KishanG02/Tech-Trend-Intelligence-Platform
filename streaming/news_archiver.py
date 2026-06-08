import json
from pathlib import Path
from datetime import datetime

from kafka import KafkaConsumer

from config.settings import (
    KAFKA_BROKER,
    NEWS_TOPIC
)

consumer = KafkaConsumer(
    NEWS_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    auto_offset_reset="latest",
    value_deserializer=lambda m: json.loads(m.decode("utf-8"))
)

Path("data-lake/raw/news/").mkdir(
    parents=True,
    exist_ok=True
)

print("Archiver running...")

for msg in consumer:

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    file_path = (
        f"data-lake/raw/news/news_{timestamp}.json"
    )

    with open(file_path, "w") as f:
        json.dump(msg.value, f, indent=4)

    print(f"Saved: {file_path}")