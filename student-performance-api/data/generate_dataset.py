"""
Generates a synthetic but realistic student performance dataset.

Kaggle requires authenticated API access which isn't available in this
environment, so this script builds a dataset with the same schema and
realistic statistical relationships as the popular Kaggle "Student
Performance" datasets. Swap this out for a real Kaggle CSV at
data/students.csv if you have API credentials -- the rest of the
pipeline (notebook, training script, API) doesn't care where the data
came from as long as the columns match.
"""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(42)
N = 1200


def generate_dataset(n=N):
    hours_studied = np.clip(RNG.normal(5, 2.2, n), 0, 12)
    attendance_percentage = np.clip(RNG.normal(78, 14, n), 30, 100)
    previous_grade = np.clip(RNG.normal(70, 15, n), 30, 100)
    sleep_hours = np.clip(RNG.normal(6.5, 1.3, n), 3, 10)
    assignments_completed = np.clip(RNG.normal(14, 4, n), 0, 20).round().astype(int)

    # Latent "score" that drives pass/fail, each feature weighted by how
    # much it plausibly affects outcomes, plus noise for realism.
    score = (
        0.35 * (hours_studied / 12)
        + 0.30 * (attendance_percentage / 100)
        + 0.20 * (previous_grade / 100)
        + 0.05 * (sleep_hours / 10)
        + 0.10 * (assignments_completed / 20)
        + RNG.normal(0, 0.08, n)
    )

    threshold = np.quantile(score, 0.38)  # ~62% pass rate
    passed = (score > threshold).astype(int)

    df = pd.DataFrame(
        {
            "hours_studied": hours_studied.round(1),
            "attendance_percentage": attendance_percentage.round(1),
            "previous_grade": previous_grade.round(1),
            "sleep_hours": sleep_hours.round(1),
            "assignments_completed": assignments_completed,
            "passed": passed,
        }
    )

    # Sprinkle a few missing values so the notebook's cleaning steps
    # have something real to do.
    for col in ["attendance_percentage", "sleep_hours"]:
        idx = RNG.choice(n, size=int(n * 0.02), replace=False)
        df.loc[idx, col] = np.nan

    return df


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("students.csv", index=False)
    print(f"Wrote {len(df)} rows to students.csv")
    print(df["passed"].value_counts(normalize=True))
