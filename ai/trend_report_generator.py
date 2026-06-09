import json
import os
from pathlib import Path
from datetime import datetime

from groq import Groq
from dotenv import load_dotenv

# =======================================
# Load Environment Variables
# =======================================

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in .env"
    )

client = Groq(
    api_key=GROQ_API_KEY
)

# =======================================
# Load Trend Data
# =======================================

ANALYTICS_PATH = Path(
    "data-lake/analytics"
)

with open(
    ANALYTICS_PATH / "unified_trend_scores.json"
) as f:

    trends = json.load(f)

top_trends = trends[:5]

# =======================================
# Build Prompt
# =======================================

trend_text = ""

for item in top_trends:

    trend_text += (
        f"{item['keyword']} "
        f"(Score: {item['final_score']})\n"
    )

prompt = f"""
You are a technology trend analyst.

Analyze these technology trends and create
a concise executive summary.

Technology Trends:

{trend_text}

Requirements:
- 5 to 8 sentences
- Professional tone
- Mention strongest trends
- Mention weaker trends
- Mention overall market direction
"""

# =======================================
# Generate Summary
# =======================================

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.4
)

summary = (
    response.choices[0]
    .message
    .content
)

# =======================================
# Save Result
# =======================================

result = {
    "generated_at":
        datetime.utcnow().isoformat(),
    "summary":
        summary
}

with open(
    ANALYTICS_PATH / "ai_summary.json",
    "w"
) as f:

    json.dump(
        result,
        f,
        indent=4
    )

print(
    "AI trend summary generated."
)