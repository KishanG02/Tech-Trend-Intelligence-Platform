import json

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

print("Listening for news...\n")

for msg in consumer:

    print("=" * 50)

    print(
        f"\nKeyword: {msg.value.get('keyword')}"
    )

    print(
        f"\nTitle: {msg.value.get('title')}"
    )

    print(
        f"\nPublished: {msg.value.get('published_at')}"
    )