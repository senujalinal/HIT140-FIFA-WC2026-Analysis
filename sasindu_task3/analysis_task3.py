from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.analysis_utils import OUTPUTS, describe, difference_ci, ensure_output_dirs, hedges_g


def main() -> None:
    source = OUTPUTS / "data" / "task3_competitiveness.csv"
    with source.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    group = np.array([float(row["absolute_goal_margin"]) for row in rows if row["stage_group"] == "group"])
    knockout = np.array([float(row["absolute_goal_margin"]) for row in rows if row["stage_group"] == "knockout"])
    t_stat, p_value = stats.ttest_ind(knockout, group, equal_var=False)
    mann_stat, mann_p = stats.mannwhitneyu(knockout, group, alternative="two-sided")

    results = {
        "question": "Were knockout matches more closely contested than group-stage matches?",
        "knockout": describe(knockout),
        "group": describe(group),
        "mean_difference_knockout_minus_group": float(knockout.mean() - group.mean()),
        "mean_difference_ci_95": difference_ci(knockout, group),
        "welch_t": float(t_stat),
        "p_value": float(p_value),
        "hedges_g": hedges_g(knockout, group),
        "shapiro_knockout_p": float(stats.shapiro(knockout).pvalue),
        "shapiro_group_p": float(stats.shapiro(group).pvalue),
        "mann_whitney_statistic": float(mann_stat),
        "mann_whitney_p": float(mann_p),
    }

    ensure_output_dirs()
    (OUTPUTS / "results" / "task3_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    figure, axis = plt.subplots(figsize=(6.4, 4.2))
    axis.boxplot([group, knockout], tick_labels=["Group", "Knockout"], patch_artist=True)
    axis.set_ylabel("Absolute goal margin")
    axis.set_title("Match competitiveness by tournament stage")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(Path(__file__).with_name("task3_competitiveness.png"), dpi=180)
    plt.close(figure)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
