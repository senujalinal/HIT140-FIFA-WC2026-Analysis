from __future__ import annotations

import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis_utils import OUTPUTS, ensure_output_dirs, is_group_match, load_matches, played_score


def main() -> None:
    rows = []
    for match_id, match in enumerate(load_matches(), start=1):
        goals1, goals2 = played_score(match)
        rows.append(
            {
                "match_id": match.get("num", match_id),
                "stage_group": "group" if is_group_match(match) else "knockout",
                "stage": match["round"],
                "absolute_goal_margin": abs(goals1 - goals2),
                "decided_by_shootout": int("p" in match["score"]),
            }
        )

    ensure_output_dirs()
    destination = OUTPUTS / "data" / "task3_competitiveness.csv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Task 3 prepared {len(rows)} match observations")
    print(f"Saved {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
