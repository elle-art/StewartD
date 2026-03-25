import os
import sys
from pathlib import Path

import pandas as pd

from quality_checks import (
    check_nulls,
    check_duplicates,
    check_negative_values,
    check_future_dates,
    check_email_format,
)
from report_generator import generate_markdown_report


def main():
    base_dir = Path(__file__).resolve().parent
    input_csv = base_dir / "sample_data.csv"
    output_md = base_dir / "output" / "report.md"

    # if path given as arg, override
    if len(sys.argv) > 1:
        input_csv = Path(sys.argv[1]).expanduser()

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    df = pd.read_csv(input_csv)

    # run quality checks
    nulls = check_nulls(df)
    duplicates = check_duplicates(df, key_column="order_id")  # assuming order_id is the key
    negative_values = check_negative_values(
        df,
        numeric_columns=[c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    )
    future_dates = (
        check_future_dates(df, date_column="order_date")
        if "order_date" in df.columns
        else {"date_column": "order_date", "future_count": 0, "future_percent": 0.0, "future_indices": [], "future_values": []}
    )
    email_format = (
        check_email_format(df, email_column="email")
        if "email" in df.columns
        else {"email_column": "email", "invalid_count": 0, "invalid_percent": 0.0, "invalid_indices": [], "invalid_values": []}
    )

    all_checks = {
        "Null Values": nulls,
        "Duplicates": duplicates,
        "Negative Values": negative_values,
        "Future Dates": future_dates,
        "Email Format": email_format,
    }

    report_md = generate_markdown_report(
        checks=all_checks,
        file_name=input_csv.name,
        total_rows=len(df),
    )

    os.makedirs(output_md.parent, exist_ok=True)
    output_md.write_text(report_md, encoding="utf-8")

    print("Data quality check complete")
    print(f"Input file: {input_csv}")
    print(f"Rows: {len(df)}")
    print(f"Report written to: {output_md}")
    # calculate total issues properly
    total_issues = (
        sum(c.get("null_count", 0) for c in nulls.values()) +
        duplicates.get("duplicate_count", 0) +
        sum(c.get("negative_count", 0) for c in negative_values.values()) +
        future_dates.get("future_count", 0) +
        email_format.get("invalid_count", 0)
    )
    print(f"Total issues: {total_issues}")

if __name__ == "__main__":
    main()