from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKFLOWS = [
    ("lahiru_task1", "data_wrangling_task1.py", "analysis_task1.py"),
    ("hansana_task2", "data_wrangling_task2.py", "analysis_task2.py"),
    ("sasindu_task3", "data_wrangling_task3.py", "analysis_task3.py"),
    ("senuja_task4", "data_wrangling_task4.py", "analysis_task4.py"),
]


def main() -> None:
    for folder, wrangling, analysis in WORKFLOWS:
        for filename in (wrangling, analysis):
            path = ROOT / folder / filename
            print(f"Running {path.relative_to(ROOT)}")
            subprocess.run([sys.executable, str(path)], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
