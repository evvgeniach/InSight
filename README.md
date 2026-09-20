# InSight

**Ask questions about your data in plain English. Get real, computed answers, charts, and business insights — powered by Claude.**

---

## What it does

Load a dataset, type a question, and InSight:
- Writes and runs real pandas code against your **full** dataset to compute the answer (not a guess from a sample)
- Returns key metrics and a chart when relevant
- Suggests smart follow-up questions
- Flags data quality issues (missing values, potential ID columns, etc.) via an automatic profile
- Maintains conversation history so you can keep drilling down
- Lets you save a workspace (dataset + conversation) and pick it back up later
- Exports the full session as an HTML or plain-text report

---

## Data sources

- **Upload** — CSV or Excel (`.csv`, `.xlsx`, `.xls`), multiple files at once
- **Google Sheets** — paste a shareable link (must be viewable by "Anyone with the link")
- **SQL database** — any SQLAlchemy connection string + a query
- **Demo dataset** — UK company records from Companies House, bundled in `demo_data/`

When more than one dataset is loaded, Claude can reference all of them (e.g. "join X and Y on company_number").

---

## Demo

> "Which product category generates the most revenue?"
> → Bar chart + breakdown by category + follow-up suggestions

> "What is the return rate and which products drive it?"
> → Computed return rate, ranked product list, recommended actions

---

## Quick start

```bash
git clone https://github.com/evvgeniach/InSight.git
cd InSight
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your API key
streamlit run app.py
```

---

## Setup

### 1. Get an Anthropic API key
Go to console.anthropic.com → API Keys → Create key

### 2. Add it to `.env`
```
ANTHROPIC_API_KEY=your-key-here
```

`COMPANIES_HOUSE_API_KEY` is only needed if you want to regenerate the demo dataset yourself via `fetch_data.py` — the app itself doesn't require it.

### 3. Run the app
```bash
streamlit run app.py
```

---

## Project structure

```
InSight/
├── app.py                  # Streamlit app entry point + UI
├── fetch_data.py           # Standalone script to (re)generate the demo dataset
├── src/
│   ├── analyser.py         # Claude API calls, prompt logic, the agentic run_python loop
│   ├── executor.py         # Sandboxed pandas code execution with a timeout
│   ├── data_loader.py      # CSV/Excel parsing, schema building
│   ├── connectors.py       # Google Sheets + SQL data loading
│   ├── profiler.py         # Column-level profiling and data quality warnings
│   ├── charts.py           # Plotly chart generation
│   ├── reporter.py         # HTML session report export
│   └── workspace.py        # Save/load/delete named workspaces (dataset + conversation)
├── demo_data/
│   └── companies_house.csv
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Saved workspaces are written to `workspaces/` at runtime (git-ignored, not part of the repo).

---

## Tech stack

- [Streamlit](https://streamlit.io) — app framework
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — LLM API
- [Pandas](https://pandas.pydata.org) — data processing
- [Plotly](https://plotly.com/python) — interactive charts
- [SQLAlchemy](https://www.sqlalchemy.org) — SQL database connections
- [openpyxl](https://openpyxl.readthedocs.io) — Excel file support
- [python-dotenv](https://pypi.org/project/python-dotenv) — environment variable management

---

## Privacy note

Your data is never stored remotely. The dataset schema and a sample of rows are sent to the Claude API for context; actual computations run locally against the full dataset, and only the resulting output (numbers, short text) is sent back to Claude to phrase the answer. Saved workspaces are written to your local disk only.

---

## Roadmap

- [ ] PDF report export
- [ ] Visual (no-code) multi-table join builder
- [ ] Scheduled/recurring reports

