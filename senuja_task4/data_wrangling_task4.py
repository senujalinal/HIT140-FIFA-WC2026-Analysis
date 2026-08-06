from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis_utils import OUTPUTS, ensure_output_dirs, is_group_match, load_matches


def main() -> None:
    matches = load_matches()
    qualifiers = {
        team
        for match in matches
        if not is_group_match(match)
        for team in (match["team1"], match["team2"])
    }
    scorers: dict[str, Counter] = defaultdict(Counter)

    for match in matches:
        if not is_group_match(match):
            continue
        for team_key, goals_key in (("team1", "goals1"), ("team2", "goals2")):
            team = match[team_key]
            scorers.setdefault(team, Counter())
            for goal in match.get(goals_key, []):
                scorers[team][goal["name"]] += 1

    rows = []
    for team, counts in sorted(scorers.items()):
        total = sum(counts.values())
        if total == 0:
            continue
        top_total = max(counts.values())
        top_scorers = sorted(name for name, value in counts.items() if value == top_total)
        rows.append(
            {
                "team": team,
                "advanced": int(team in qualifiers),
                "group_stage_goals": total,
                "unique_scorers": len(counts),
                "top_scorer_goals": top_total,
                "top_scorer_names": "; ".join(top_scorers),
                "top_scorer_share": top_total / total,
            }
        )

    ensure_output_dirs()
    destination = OUTPUTS / "data" / "task4_scoring_concentration.csv"
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Task 4 prepared {len(rows)} team observations with at least one group-stage goal")
    print(f"Saved {destination.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
