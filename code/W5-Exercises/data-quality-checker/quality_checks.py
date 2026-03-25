import re
from datetime import datetime

import pandas as pd


def check_nulls(df: pd.DataFrame) -> dict:
    """Check for null values in each column."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")

    result = {}
    row_count = len(df)
    for col in df.columns:
        null_count = df[col].isna().sum()
        result[col] = {
            "null_count": int(null_count),
            "null_percent": float(0 if row_count == 0 else null_count / row_count * 100),
        }
    return result


def check_duplicates(df: pd.DataFrame, key_column: str) -> dict:
    """Find duplicate rows based on a key column."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if key_column not in df.columns:
        raise ValueError(f"{key_column} is not in DataFrame columns")

    dup_mask = df.duplicated(subset=[key_column], keep=False)
    dup_df = df[dup_mask]
    dup_count = int(dup_df.shape[0])

    return {
        "key_column": key_column,
        "duplicate_count": dup_count,
        "duplicate_values": dup_df[key_column].dropna().unique().tolist(),
        "duplicate_indices": dup_df.index.tolist(),
    }


def check_negative_values(df: pd.DataFrame, numeric_columns: list) -> dict:
    """Flag negative values in specified numeric columns."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if not isinstance(numeric_columns, list):
        raise TypeError("numeric_columns must be a list")

    result = {}
    for col in numeric_columns:
        if col not in df.columns:
            result[col] = {"error": "column not found"}
            continue

        col_vals = pd.to_numeric(df[col], errors="coerce")
        neg_mask = col_vals < 0
        neg_count = int(neg_mask.sum())

        result[col] = {
            "negative_count": neg_count,
            "negative_percent": float(0 if len(df) == 0 else neg_count / len(df) * 100),
            "negative_indices": df.index[neg_mask].tolist(),
        }

    return result


def check_future_dates(df: pd.DataFrame, date_column: str) -> dict:
    """Check for dates in the future."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if date_column not in df.columns:
        raise ValueError(f"{date_column} is not in DataFrame columns")

    dates = pd.to_datetime(df[date_column], errors="coerce")
    now = pd.Timestamp(datetime.utcnow())
    future_mask = dates > now

    future_count = int(future_mask.sum())
    future_indices = df.index[future_mask].tolist()
    future_values = dates[future_mask].apply(lambda d: d.isoformat() if pd.notna(d) else None).tolist()

    return {
        "date_column": date_column,
        "future_count": future_count,
        "future_percent": float(0 if len(df) == 0 else future_count / len(df) * 100),
        "future_indices": future_indices,
        "future_values": future_values,
    }


def check_email_format(df: pd.DataFrame, email_column: str) -> dict:
    """Validate email format in the specified column."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df must be a pandas DataFrame")
    if email_column not in df.columns:
        raise ValueError(f"{email_column} is not in DataFrame columns")

    pattern = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

    emails = df[email_column].astype(str)
    valid_mask = emails.apply(
        lambda v: bool(pattern.match(v)) if pd.notna(v) and v.strip() != "nan" else False
    )
    invalid_mask = ~valid_mask

    invalid_count = int(invalid_mask.sum())
    invalid_indices = df.index[invalid_mask].tolist()
    invalid_values = emails[invalid_mask].replace("nan", pd.NA).tolist()

    return {
        "email_column": email_column,
        "invalid_count": invalid_count,
        "invalid_percent": float(0 if len(df) == 0 else invalid_count / len(df) * 100),
        "invalid_indices": invalid_indices,
        "invalid_values": invalid_values,
    }
    