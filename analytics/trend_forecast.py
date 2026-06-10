from pathlib import Path
import pandas as pd
from sklearn.linear_model import LinearRegression

# ====================================
# Paths
# ====================================

ANALYTICS_PATH = Path("data-lake/analytics")

HISTORY_FILE = (
    ANALYTICS_PATH /
    "trend_history.csv"
)

FORECAST_FILE = (
    ANALYTICS_PATH /
    "trend_forecast.csv"
)

# ====================================
# Load history
# ====================================

df = pd.read_csv(HISTORY_FILE)

df["date"] = pd.to_datetime(
    df["date"]
)

forecast_rows = []

# ====================================
# Forecast per keyword
# ====================================

for keyword in df["keyword"].unique():

    keyword_df = df[
        df["keyword"] == keyword
    ].copy()

    keyword_df = keyword_df.sort_values(
        "date"
    )

    # Need at least 2 points
    if len(keyword_df) < 2:
        continue

    keyword_df["x"] = range(
        len(keyword_df)
    )

    X = keyword_df[["x"]]
    y = keyword_df["final_score"]

    model = LinearRegression()

    model.fit(X, y)

    future_x = range(
        len(keyword_df),
        len(keyword_df) + 7
    )

    predictions = model.predict(
        pd.DataFrame({"x": future_x})
    )

    last_timestamp = (
        keyword_df["date"]
        .max()
    )

    for i, pred in enumerate(
        predictions,
        start=1
    ):

        forecast_rows.append({
            "date":
                last_timestamp +
                pd.Timedelta(days=i),

            "keyword":
                keyword,

            "predicted_score":
                round(float(pred), 2)
        })

# ====================================
# Save
# ====================================

forecast_df = pd.DataFrame(
    forecast_rows
)

forecast_df.to_csv(
    FORECAST_FILE,
    index=False
)

print(
    f"Saved {len(forecast_df)} forecast records."
)