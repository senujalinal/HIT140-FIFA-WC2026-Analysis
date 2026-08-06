from __future__ import annotations

import csv
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis_utils import OUTPUTS, ensure_output_dirs, is_group_match, load_matches, regulation_score


HOSTS = {"Canada", "Mexico", "USA"}
RANDOM_SEED = 140


def match_points(goals_for: int, goals_against: int) -> int:
    if goals_for > goals_against:
        return 3
    if goals_for == goals_against:
        return 1
    return 0


def main() -> None:
    host_rows = []
    comparison_candidates = []

    for match_id, match in enumerate(load_matches(), start=1):
        if not is_group_match(match):
            continue
        goals1, goals2 = regulation_score(match)
        teams = ((match["team1"], goals1, goals2), (match["team2"], goals2, goals1))
        host_teams = [team for team in teams if team[0] in HOSTS]

        if host_teams:
            for team, goals_for, goals_against in host_teams:
                host_rows.append(
                    {
                        "match_id": match.get("num", match_id),
                        "group": "host",
                        "team": team,
                        "points": match_points(goals_for, goals_against),
                    }
                )
        else:
            comparison_candidates.append((match_id, match, teams))

    generator = random.Random(RANDOM_SEED)
    comparison_rows = []
    for match_id, match, teams in comparison_candidates:
        team, goals_for, goals_against = generator.choice(teams)
        comparison_rows.append(
            {
                "match_id": match.get("num", match_id),
                "group": "comparison",
                "team": team,
                "points": match_points(goals_for, goals_against),
            }
        )

    rows = host_rows + comparison_rows
    ensure_output_dirs()
    destination = OUTPUTS / "data" / "task2_host_points.csv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Task 2 prepared {len(host_rows)} host observations and {len(comparison_rows)} independent comparison observations")
    print(f"Comparison sampling seed: {RANDOM_SEED}")
    print(f"Saved {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
