# HIT140 Foundations of Data Science group project

This repository contains the four analyses required for Objective 1 of the FIFA World Cup 2026 group project. Each task uses a different unit of investigation and follows the same reproducible workflow: data validation, preparation, descriptive statistics, a 95% confidence interval, a one-sample or two-sample t-test, an assumption check, and a non-parametric sensitivity test.

## Research questions and ownership

| Task | Research question | Member |
|---|---|---|
| 1 | Were more regulation-time goals scored after half-time than before half-time? | Lahiru Samarasinghage |
| 2 | Did the three host nations earn more group-stage points per match than a reproducible comparison sample? | Thulith Hansana |
| 3 | Were knockout matches more closely contested than group-stage matches? | Sasindu Dilshan Ranwadana |
| 4 | Was group-stage scoring concentration different for teams that advanced to the knockout stage? | Senuja Berandeniya Aluthage |

The questions are deliberately distinct. They examine goal timing, host-team results, match competitiveness, and the distribution of scoring across players.

## Repository structure

```text
data/
  raw/worldcup_2026.json
  SOURCES.md
src/
  analysis_utils.py
scripts/
  fetch_data.py
lahiru_task1/
hansana_task2/
sasindu_task3/
senuja_task4/
run_all.py
requirements.txt
```

Each member folder contains one data-wrangling script, one analysis script, one report section, and the chart referenced by that report. Presentation scripts and Objective 2 regression models are excluded because the supplied assessment instructions require Objective 1 only.

## Reproduce the analysis

Create a Python environment, install the dependencies, and run the complete workflow:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 run_all.py
```

The workflow writes cleaned tables and statistical summaries to `outputs/`. That directory is reproducible . Each analysis also refreshes the presentation-ready chart stored in its member folder.

To refresh the source snapshot before re-running the analysis:

```bash
python3 scripts/fetch_data.py
python3 run_all.py
```

## Interpretation rules

All tests are two-sided at an alpha level of 0.05. Confidence intervals use the t distribution. A statistically significant result is not treated as proof of causation. The reports discuss design limitations, dependence risks, distributional assumptions, and the corresponding sensitivity test.

## Collaboration evidence

Git history should record work completed or genuinely reviewed by each member. The group should also retain ordinary collaboration evidence, such as meeting notes, team-chat decisions, peer-review comments, and a simple task allocation record. Although we planned earlier, Jira and Confluence are not used for this project. 
