import re
import pandas as pd


def load_from_sql(connection_string: str, query: str) -> pd.DataFrame:
    try:
        from sqlalchemy import create_engine, text
    except ImportError:
        raise ImportError("sqlalchemy is required for SQL connections. Run: pip install sqlalchemy")
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        return pd.read_sql(text(query), conn)


def load_from_google_sheets(url: str) -> pd.DataFrame:
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", url)
    if not match:
        raise ValueError(
            "Could not parse the Google Sheets URL. "
            "Copy the URL directly from your browser address bar."
        )
    sheet_id = match.group(1)
    gid_match = re.search(r"gid=(\d+)", url)
    gid = gid_match.group(1) if gid_match else "0"

    csv_url = (
        f"https://docs.google.com/spreadsheets/d/{sheet_id}"
        f"/export?format=csv&gid={gid}"
    )
    try:
        return pd.read_csv(csv_url)
    except Exception as exc:
        raise ValueError(
            f"Could not load the sheet — make sure it is shared as "
            f"'Anyone with the link can view'. Detail: {exc}"
        )
