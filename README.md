# InSight

**Ask questions about your data in plain English. Get instant analysis, charts, and business insights — powered by Claude.**

---

## What it does

Upload a CSV or Excel file, type a question, and InSight:
- Computes the answer directly from your data
- Returns key metrics and a chart when relevant
- Suggests smart follow-up questions
- Maintains conversation history so you can keep drilling down
- Exports a full report of your session

---

## Demo

> "Which product category generates the most revenue?"
> → Bar chart + breakdown by category + follow-up suggestions

> "What is the return rate and which products drive it?"
> → Computed return rate, ranked product list, recommended actions

---

## Quick start

```bash
git clone https://github.com/yourusername/insight
cd insight
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

### 2. Add it to .env
```
ANTHROPIC_API_KEY=your-key-here
```

### 3. Run the app
```bash
streamlit run app.py
```

---

## Project structure

```
insight/
├── app.py                  # Streamlit app entry point
├── src/
│   ├── analyser.py         # Claude API calls + prompt logic
│   ├── data_loader.py      # CSV/Excel parsing, schema building
│   └── charts.py           # Plotly chart generation
├── demo_data/
│   ├── ecommerce.csv
│   ├── marketing.csv
│   └── finance.csv
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Tech stack

- [Streamlit](https://streamlit.io) — app framework
- [Anthropic Python SDK](https://github.com/anthropics/anthropic-sdk-python) — LLM API
- [Pandas](https://pandas.pydata.org) — data processing
- [Plotly](https://plotly.com/python) — interactive charts
- [Python-dotenv](https://pypi.org/project/python-dotenv) — environment variable management

---

## Privacy note

Your data is never stored. The dataset schema and a sample of rows are sent to the Claude API to generate answers — the full dataset stays in your session only.

---

## Roadmap

- [ ] Excel file support
- [ ] PDF report export
- [ ] Multi-table joins
- [ ] Saved sessions

