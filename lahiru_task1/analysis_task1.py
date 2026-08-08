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

from src.analysis_utils import OUTPUTS, describe, ensure_output_dirs, mean_ci


def main() -> None:
    source = OUTPUTS / "data" / "task1_goal_timing.csv"
    with source.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    first = np.array([float(row["first_half_goals"]) for row in rows])
    second = np.array([float(row["second_half_goals"]) for row in rows])
    differences = second - first

    t_stat, p_value = stats.ttest_1samp(differences, popmean=0)
    shapiro_stat, shapiro_p = stats.shapiro(differences)
    wilcoxon_stat, wilcoxon_p = stats.wilcoxon(differences)
    interval = mean_ci(differences)
    effect_size = float(differences.mean() / differences.std(ddof=1))

    results = {
        "question": "Were more regulation-time goals scored after half-time than before half-time?",
        "first_half": describe(first),
        "second_half": describe(second),
        "mean_difference": float(differences.mean()),
        "mean_difference_ci_95": interval,
        "one_sample_t": float(t_stat),
        "p_value": float(p_value),
        "cohens_dz": effect_size,
        "shapiro_p": float(shapiro_p),
        "wilcoxon_statistic": float(wilcoxon_stat),
        "wilcoxon_p": float(wilcoxon_p),
    }

    ensure_output_dirs()
    result_path = OUTPUTS / "results" / "task1_results.json"
    result_path.write_text(json.dumps(results, indent=2), encoding="utf-8")

    first_ci = mean_ci(first)
    second_ci = mean_ci(second)
    means = [first.mean(), second.mean()]
    errors = [first.mean() - first_ci[0], second.mean() - second_ci[0]]
    figure, axis = plt.subplots(figsize=(7.0, 4.4))
    axis.bar(
        ["First half", "Second half"],
        means,
        yerr=errors,
        capsize=5,
        color=["#315b7d", "#d9822b"],
    )
    axis.set_ylabel("Mean goals per match")
    axis.set_title("Regulation-time scoring by half")
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(Path(__file__).with_name("task1_goal_timing.png"), dpi=180)
    plt.close(figure)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
