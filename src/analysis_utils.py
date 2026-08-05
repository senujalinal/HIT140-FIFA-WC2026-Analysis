from __future__ import annotations

import json
from pathlib import Path
from statistics import mean, median, stdev

import numpy as np
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
RAW_DATA = ROOT / "data" / "raw" / "worldcup_2026.json"
OUTPUTS = ROOT / "outputs"


def load_matches(path: Path = RAW_DATA) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    matches = payload.get("matches")
    if not isinstance(matches, list) or len(matches) != 104:
        raise ValueError("Expected a 104-match World Cup dataset")

    required = {"round", "date", "team1", "team2", "score", "ground"}
    for index, match in enumerate(matches, start=1):
        missing = required.difference(match)
        if missing:
            raise ValueError(f"Match {index} is missing: {sorted(missing)}")
        if "ft" not in match["score"] or "ht" not in match["score"]:
            raise ValueError(f"Match {index} has incomplete score data")
    return matches


def is_group_match(match: dict) -> bool:
    return match["round"].startswith("Matchday")


def played_score(match: dict) -> tuple[int, int]:
    score = match["score"]
    values = score.get("et", score["ft"])
    return int(values[0]), int(values[1])


def regulation_score(match: dict) -> tuple[int, int]:
    values = match["score"]["ft"]
    return int(values[0]), int(values[1])


def describe(values) -> dict[str, float]:
    sample = [float(value) for value in values]
    if len(sample) < 2:
        raise ValueError("At least two observations are required")
    return {
        "n": len(sample),
        "mean": mean(sample),
        "median": median(sample),
        "sd": stdev(sample),
        "min": min(sample),
        "max": max(sample),
    }


def mean_ci(values, confidence: float = 0.95) -> tuple[float, float]:
    sample = np.asarray(values, dtype=float)
    standard_error = stats.sem(sample)
    return tuple(
        float(value)
        for value in stats.t.interval(
            confidence,
            df=len(sample) - 1,
            loc=float(sample.mean()),
            scale=float(standard_error),
        )
    )


def difference_ci(first, second, confidence: float = 0.95) -> tuple[float, float]:
    a = np.asarray(first, dtype=float)
    b = np.asarray(second, dtype=float)
    difference = float(a.mean() - b.mean())
    variance = a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b)
    standard_error = float(np.sqrt(variance))
    degrees = variance**2 / (
        (a.var(ddof=1) / len(a)) ** 2 / (len(a) - 1)
        + (b.var(ddof=1) / len(b)) ** 2 / (len(b) - 1)
    )
    critical = stats.t.ppf((1 + confidence) / 2, degrees)
    return difference - critical * standard_error, difference + critical * standard_error


def hedges_g(first, second) -> float:
    a = np.asarray(first, dtype=float)
    b = np.asarray(second, dtype=float)
    degrees = len(a) + len(b) - 2
    pooled = np.sqrt(
        ((len(a) - 1) * a.var(ddof=1) + (len(b) - 1) * b.var(ddof=1))
        / degrees
    )
    correction = 1 - 3 / (4 * degrees - 1)
    return float(correction * (a.mean() - b.mean()) / pooled)


def ensure_output_dirs() -> None:
    (OUTPUTS / "data").mkdir(parents=True, exist_ok=True)
    (OUTPUTS / "results").mkdir(parents=True, exist_ok=True)
    (OUTPUTS / "figures").mkdir(parents=True, exist_ok=True)
