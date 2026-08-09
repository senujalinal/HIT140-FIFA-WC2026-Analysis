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

from src.analysis_utils import OUTPUTS, describe, difference_ci, ensure_output_dirs, hedges_g, mean_ci


def main() -> None:
    source = OUTPUTS / "data" / "task2_host_points.csv"
    with source.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    host = np.array([float(row["points"]) for row in rows if row["group"] == "host"])
    comparison = np.array([float(row["points"]) for row in rows if row["group"] == "comparison"])
    t_stat, p_value = stats.ttest_ind(host, comparison, equal_var=False)
    shapiro_host = stats.shapiro(host).pvalue
    shapiro_comparison = stats.shapiro(comparison).pvalue
    mann_stat, mann_p = stats.mannwhitneyu(host, comparison, alternative="two-sided")

    results = {
        "question": "Did the host nations earn more group-stage points per match than the comparison sample?",
        "host": describe(host),
        "comparison": describe(comparison),
        "mean_difference": float(host.mean() - comparison.mean()),
        "mean_difference_ci_95": difference_ci(host, comparison),
        "welch_t": float(t_stat),
        "p_value": float(p_value),
        "hedges_g": hedges_g(host, comparison),
        "shapiro_host_p": float(shapiro_host),
        "shapiro_comparison_p": float(shapiro_comparison),
        "mann_whitney_statistic": float(mann_stat),
        "mann_whitney_p": float(mann_p),
    }

    ensure_output_dirs()
    (OUTPUTS / "results" / "task2_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    host_ci = mean_ci(host)
    comparison_ci = mean_ci(comparison)
    errors = [host.mean() - host_ci[0], comparison.mean() - comparison_ci[0]]
    figure, axis = plt.subplots(figsize=(7.0, 4.4))
    axis.bar(
        ["Hosts", "Comparison sample"],
        [host.mean(), comparison.mean()],
        yerr=errors,
        capsize=5,
        color=["#2f855a", "#718096"],
    )
    axis.set_ylabel("Mean group-stage points per match")
    axis.set_ylim(0, 3)
    axis.set_title("Host-nation performance")
    axis.tick_params(axis="x", labelsize=10)
    axis.spines[["top", "right"]].set_visible(False)
    figure.tight_layout()
    figure.savefig(Path(__file__).with_name("task2_host_points.png"), dpi=180)
    plt.close(figure)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
