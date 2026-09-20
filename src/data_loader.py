import pandas as pd


def load_file(file):
    name = getattr(file, 'name', str(file))
    if str(name).endswith(('.xlsx', '.xls')):
        return pd.read_excel(file)
    try:
        return pd.read_csv(file, encoding='utf-8')
    except UnicodeDecodeError:
        if hasattr(file, 'seek'):
            file.seek(0)
        return pd.read_csv(file, encoding='latin-1')


load_csv = load_file


def build_schema(df):
    lines = []
    for col in df.columns:
        dtype = "num" if pd.api.types.is_numeric_dtype(df[col]) else "str"
        sample = df[col].dropna().head(3).tolist()
        lines.append(f"{col} ({dtype}): e.g. {sample}")
    return "\n".join(lines)


def get_sample(df):
    return df.head(5).to_json(orient="records")


def get_summary(df):
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "column_names": df.columns.tolist()
    }


def build_multi_schema(datasets: dict, active_key: str) -> str:
    parts = [f"ACTIVE DATASET: {active_key}\n{build_schema(datasets[active_key])}"]
    others = {k: v for k, v in datasets.items() if k != active_key}
    if others:
        parts.append("\nOTHER AVAILABLE DATASETS (accessible in Python via datasets['name']):")
        for name, df in others.items():
            parts.append(f"\n{name}:\n{build_schema(df)}")
    return "\n".join(parts)
