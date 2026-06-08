import json
import os
from datetime import datetime

import requests
from kafka import KafkaProducer

from config.settings import (
    KAFKA_BROKER,
    NEWS_TOPIC
)

from config.env_loader import *

NEWS_API_KEY = os.getenv("NEWS_API_KEY")

if not NEWS_API_KEY:
    raise ValueError(
        "NEWS_API_KEY not found in .env file"
    )

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

KEYWORDS = [
    "Artificial Intelligence",
    "AWS",
    "Azure",
    "Databricks",
    "Kafka",
    "Cloud Computing"
]


def fetch_news(keyword):
    """
    Fetch latest news articles for a keyword.
    """

    url = "https://newsapi.org/v2/everything"

    params = {
        "q": keyword,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        print(f"Failed to fetch news for {keyword}")
        return []

    return response.json().get("articles", [])


def send_to_kafka(article, keyword):

    message = {
        "source": "newsapi",
        "keyword": keyword,
        "ingestion_timestamp": datetime.utcnow().isoformat(),

        "title": article.get("title"),
        "description": article.get("description"),
        "published_at": article.get("publishedAt"),
        "url": article.get("url")
    }

    producer.send(
        NEWS_TOPIC,
        message
    )


def main():

    for keyword in KEYWORDS:

        print(f"\nFetching news for: {keyword}")

        articles = fetch_news(keyword)

        for article in articles:

            send_to_kafka(
                article,
                keyword
            )

            print(
                f"Sent: {article.get('title', 'No Title')}"
            )

    producer.flush()

    print("\nNews ingestion completed.")


if __name__ == "__main__":
    main()