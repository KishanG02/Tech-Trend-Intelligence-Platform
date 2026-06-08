import subprocess

steps = [
    ("News Producer", "python -m streaming.news_producer"),
    ("News Validator", "python -m processing.news_validator"),
    ("News Analytics", "python -m analytics.news_metrics")
]

for step_name, command in steps:

    print(f"\n{'=' * 60}")
    print(f"Running: {step_name}")
    print(f"{'=' * 60}")

    result = subprocess.run(
        command,
        shell=True
    )

    if result.returncode != 0:
        raise Exception(
            f"{step_name} failed."
        )

print("\nPipeline completed successfully.")