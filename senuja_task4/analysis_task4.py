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
    source = OUTPUTS / "data" / "task4_scoring_concentration.csv"
    with source.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    advanced = np.array([float(row["top_scorer_share"]) for row in rows if row["advanced"] == "1"])
    eliminated = np.array([float(row["top_scorer_share"]) for row in rows if row["advanced"] == "0"])
    t_stat, p_value = stats.ttest_ind(advanced, eliminated, equal_var=False)
    mann_stat, mann_p = stats.mannwhitneyu(advanced, eliminated, alternative="two-sided")

    results = {
        "question": "Was group-stage scoring concentration different for teams that advanced?",
        "advanced": describe(advanced),
        "eliminated": describe(eliminated),
        "mean_difference_advanced_minus_eliminated": float(advanced.mean() - eliminated.mean()),
        "mean_difference_ci_95": difference_ci(advanced, eliminated),
        "welch_t": float(t_stat),
        "p_value": float(p_value),
        "hedges_g": hedges_g(advanced, eliminated),
        "shapiro_advanced_p": float(stats.shapiro(advanced).pvalue),
        "shapiro_eliminated_p": float(stats.shapiro(eliminated).pvalue),
        "mann_whitney_statistic": float(mann_stat),
        "mann_whitney_p": float(mann_p),
    }

    ensure_output_dirs()
    (OUTPUTS / "results" / "task4_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    figure, axis = plt.subplots(figsize=(7.0, 4.4))
    axis.boxplot([advanced, eliminated], tick_labels=["Advanced", "Eliminated"], patch_artist=True)
    axis.set_ylabel("Top scorer's share of team goals")
    axis.set_title("Group-stage scoring concentration")
    axis.tick_params(axis="x", labelsize=10)
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(Path(__file__).with_name("task4_scoring_concentration.png"), dpi=180)
    plt.close(figure)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
