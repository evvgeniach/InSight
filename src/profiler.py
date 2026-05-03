import pandas as pd


def generate_profile(df):
    profile = {}
    for col in df.columns:
        series = df[col]
        all_null = series.isna().all()
        info = {
            "null_pct": round(series.isna().mean() * 100, 1),
            "unique": series.nunique(),
        }
        if pd.api.types.is_numeric_dtype(series):
            info["kind"] = "numeric"
            info["min"] = series.min() if not all_null else "N/A"
            info["max"] = series.max() if not all_null else "N/A"
            info["mean"] = round(series.mean(), 2) if not all_null else "N/A"
            info["median"] = round(series.median(), 2) if not all_null else "N/A"
        else:
            info["kind"] = "categorical"
            vc = series.value_counts()
            info["top"] = vc.head(5).to_dict()
        profile[col] = info
    return profile


def get_quality_warnings(df):
    warnings = []
    for col in df.columns:
        pct = df[col].isna().mean() * 100
        if pct >= 50:
            warnings.append(("error", f"**{col}**: {pct:.0f}% missing values"))
        elif pct >= 10:
            warnings.append(("warning", f"**{col}**: {pct:.0f}% missing values"))
    dupes = df.duplicated().sum()
    if dupes > 0:
        warnings.append(("warning", f"{dupes:,} duplicate rows detected"))
    return warnings


def detect_time_columns(df):
    cols = []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            cols.append(col)
        elif df[col].dtype == object:
            sample = df[col].dropna().head(30)
            try:
                parsed = pd.to_datetime(sample)
                if parsed.notna().mean() > 0.8:
                    cols.append(col)
            except Exception:
                pass
    return cols


def generate_starter_questions(df):
    numeric = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    cat = [c for c in df.columns if not pd.api.types.is_numeric_dtype(df[c])]
    time_cols = detect_time_columns(df)

    questions = [
        "Summarise this dataset for me",
        "What are the most interesting insights in this data?",
    ]

    if numeric and cat:
        questions.append(f"Which {cat[0]} has the highest {numeric[0]}?")
        questions.append(f"Show me {numeric[0]} broken down by {cat[0]}")

    if len(numeric) >= 2:
        questions.append(f"Is there a correlation between {numeric[0]} and {numeric[1]}?")

    if time_cols and numeric:
        questions.append(f"How has {numeric[0]} changed over time?")
    elif cat:
        questions.append(f"What is the distribution of {cat[0]}?")

    return questions[:6]
