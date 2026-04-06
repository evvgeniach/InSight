import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def load_csv(file):
    return pd.read_csv(file)

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