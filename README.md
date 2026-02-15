# LLM Generation of Intentionally Vulnerable Dockerfiles

This repository contains the full experimental artifacts for a two-phase empirical study on LLM-assisted generation of intentionally vulnerable containerized environments for cyber ranges.

The study evaluates whether LLMs can generate environments that are:
- buildable,
- runnable,
- exploitable with known public exploits,

and compares deployment strategies by repair effort and automation difficulty.

## Safety and ethics

All artifacts target known vulnerable versions for controlled research only.
Use only in isolated, non-production environments.

## Repository structure

```text
.
├── Dockerfiles/
│   ├── 1_ModelSelection/
│   ├── 2_ModelExperiment/
│   ├── Shared.mk
│   └── Preflight.mk
├── Analysis/
│   ├── Phase1_Results_with_WES.csv
│   ├── Phase2RawAnalysis_*.xlsx
│   ├── Phase2TableSummary*.xlsx
│   ├── tables_paper/
│   ├── latex_tables/
│   ├── figures_paper/
│   └── phase1_analysis.py / phase2_figures.py
├── Experiment/
│   ├── 1_Pilot Study/
│   └── 2_Main Experiment/
└── docs/
```

## Dockerfiles folder organization

### `Dockerfiles/1_ModelSelection`

Phase 1 (pilot model selection). Each scenario is under a `CVE-*` folder. Inside each CVE, generations are organized by model folder name:

- `Bing`
- `Gemini`
- `Gemini3-Pro`
- `Gpt3.5`
- `Gpt5.2-Thinking`
- `Gpt5.2-Thinking-Web`

Additional per-CVE folders usually include:
- `Human` or `HumanFix` (reference implementation)
- `Logs` (build/run logs)
- `Exploit` (when available)
- `Diffs` (when generated)

### `Dockerfiles/2_ModelExperiment`

Phase 2 (in-depth analysis of the selected model, Gemini3-Pro).

- `LinuxServices/CVE-*`: service scenarios, typically with:
  - `Gemini3-Pro/Package` and `Gemini3-Pro/Source`
  - `Gemini3-Pro-Fixed/...` (repaired versions)
  - `Human`, `LLM`, `Logs`, `Exploit`
- `WebApps/...`: web scenarios with bundle/compose variants and corresponding logs/fixes.

Note: the `WebApps` tree includes active Phase 2 material plus historical/legacy subtrees (for example `LLM/` and `outdated/`). The paper-ready aggregates are in `Analysis/Phase2TableSummaryWeb.xlsx` and `Analysis/Phase2RawAnalysis_Web_Classified.xlsx`.

## Methodology (paper-aligned)

### Study design

The protocol follows a standard empirical software engineering workflow (planning, design, execution, analysis) with a two-phase design:

- Phase 1: pilot model selection.
- Phase 2: in-depth evaluation of the selected model.

Unit of analysis: one vulnerability scenario tied to one CVE.
Datasets were frozen before execution for comparability.

### Planning

- Scope: LLM generation of intentionally vulnerable Dockerized environments.
- Sampling: stratified by application type (web applications vs system services).
- Sources: public CVE/exploit references and vulnerable container references.
- Valid scenario definition: builds, runs, and is exploitable with the known public exploit.

### Design

#### Models (Phase 1)

- GPT-3.5 (offline)
- Bing Chat (web-enabled)
- Gemini (web-enabled)
- Gemini3-Pro (web-enabled)
- GPT-5.2 Thinking (offline)
- GPT-5.2 Thinking Web (web-enabled)

#### Prompting constraints

- Zero-shot prompting
- Single-pass generation
- No file reading of repository artifacts by the model
- Chat-interface interactions (no fixed API snapshot)

Web-enabled vs offline was treated as an experimental condition in Phase 1.

#### Metrics

##### Phase 1: Weighted Error Score (WES)

Execution penalty:

- `E = 0` if build=1 and run=1
- `E = 1` if build=1 and run=0
- `E = 2` if build=0

Fix severity: `F in {0,1,2,3}`

With `L=3`,

`WES = (L+1) * E + F = 4E + F`

Range: `0..11`.

##### Phase 2: repair taxonomy

Two orthogonal dimensions:

- Change impact: `C0, C1, C2` with weighted score
  - `ImpactScore = sum(nC0*1 + nC1*3 + nC2*6)`
- Automation challenge: `A0, A1, A2` with weighted score
  - `AutomationScore = sum(nA0*0 + nA1*1 + nA2*2)`

Outcomes tracked per scenario: build, run, exploit.

### Execution and data collection

- Environment used in the study: Ubuntu 24.04.1 LTS, Docker Engine 28.2.2, Docker Compose v2.29.7, Python 3.12.8.
- Per-scenario execution artifacts include generated Dockerfiles, logs, and exploit assets.
- Error tracking used a two-step process:
  - lightweight real-time repair logging,
  - detailed post-hoc classification by stage/category/impact/automation.

### Analysis and reporting

`Analysis/` contains:
- raw and classified spreadsheets,
- scripts to compute summary tables,
- scripts to generate publication figures,
- LaTeX-ready tables.

## Results snapshot

### Phase 1 (model selection)

From the provided paper section (54 scenarios, 6 models × 9 CVEs):

- Build success rate: **33.3%**
- Run success rate: **27.8%**
- Perfect execution (`WES=0`): **24.1%**
- Build failure rate: **70.4%**
- Mean WES: **5.67**
- Median WES: **7.00**
- Std Dev WES: **3.43**

Legacy (2024) vs modern (2026):
- Build failure: **81.5%** vs **51.9%**
- Perfect execution: **11.1%** vs **37.0%**
- Mean WES: **6.88** vs **4.46**

Selected model for Phase 2: **Gemini3-Pro** (lowest mean WES in Phase 1).

### Phase 2 (in-depth evaluation of Gemini3-Pro)

From `Analysis/tables_paper/` and summary workbooks:

- Analyzed scenarios: **40** total
  - Services: **24** (12 CVEs × package/source)
  - Web: **16** (9 compose, 7 bundle; refusal cases excluded)

Functional outcomes:
- Overall: build **20/40 (50.0%)**, run **15/40 (37.5%)**, exploit **4/40 (10.0%)**
- Services package: build **8/12 (66.7%)**, run **5/12 (41.7%)**, exploit **1/12 (8.3%)**
- Services source: build **7/12 (58.3%)**, run **5/12 (41.7%)**, exploit **1/12 (8.3%)**
- Web compose: build **4/9 (44.4%)**, run **4/9 (44.4%)**, exploit **2/9 (22.2%)**
- Web bundle: build **1/7 (14.3%)**, run **1/7 (14.3%)**, exploit **0/7 (0.0%)**

## Reproducibility quick start

### Prerequisites

- Docker Engine + Docker Compose
- GNU Make
- Python 3 (for analysis scripts)

### Run one CVE scenario (example)

```bash
cd Dockerfiles/1_ModelSelection/CVE-2019-17240
make build-gemini3-pro-single
make run-gemini3-pro-single
```

Other targets are defined in `Dockerfiles/Shared.mk` and `Dockerfiles/Preflight.mk` (including compose, package/source, and preflight variants).

### Generate analysis outputs

```bash
cd Analysis
./.venv/bin/python phase1_analysis.py
./.venv/bin/python phase2_figures.py --vector
```

Main outputs:
- CSV tables: `Analysis/tables_paper/`
- LaTeX tables: `Analysis/latex_tables/`
- Figures: `Analysis/figures_paper/`

### Key files

- Phase 1 raw+WES: `Analysis/Phase1_Results_with_WES.csv`
- Phase 2 summary (services): `Analysis/Phase2TableSummaryServices.xlsx`
- Phase 2 summary (web): `Analysis/Phase2TableSummaryWeb.xlsx`
- Phase 2 classified logs: `Analysis/Phase2RawAnalysis_Services_Classified.xlsx`, `Analysis/Phase2RawAnalysis_Web_Classified.xlsx`
- Ethical refusals log: `Analysis/Phase2EthicalFailures.xlsx`

## Citation and provenance

This repository accompanies the paper methodology and results on LLM-based generation of intentionally vulnerable Docker environments.
It includes prompts, generated artifacts, logs, classifications, and figure/table generation code to support replication and auditability.
