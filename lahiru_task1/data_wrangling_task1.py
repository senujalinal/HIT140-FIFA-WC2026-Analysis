from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis_utils import OUTPUTS, ensure_output_dirs, load_matches, regulation_score


def main() -> None:
    rows = []
    for match_id, match in enumerate(load_matches(), start=1):
        half_time = sum(int(value) for value in match["score"]["ht"])
        full_time = sum(regulation_score(match))
        second_half = full_time - half_time
        if second_half < 0:
            raise ValueError(f"Negative second-half total in match {match_id}")
        rows.append(
            {
                "match_id": match.get("num", match_id),
                "stage": match["round"],
                "first_half_goals": half_time,
                "second_half_goals": second_half,
                "second_minus_first": second_half - half_time,
            }
        )

    ensure_output_dirs()
    destination = OUTPUTS / "data" / "task1_goal_timing.csv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Task 1 prepared {len(rows)} match observations")
    print(f"Saved {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
