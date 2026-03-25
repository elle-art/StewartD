import csv
from datetime import datetime, timedelta
from pathlib import Path

OUTPUT_FILE = Path(__file__).resolve().parent/"sample_data.csv"

def main():
    fieldnames = [
        "order_id",
        "customer_name",
        "email",
        "order_date",
        "amount",
        "status",
    ]

    rows = []

    # Base valid statuses
    valid_statuses = ["pending", "completed", "cancelled"]

    # 1. Create 50 base valid rows
    base_date = datetime(2024, 1, 1)
    for i in range(1, 51):
        row = {
            "order_id": f"ORD{i:04d}",
            "customer_name": f"Customer {i}",
            "email": f"customer{i}@example.com",
            "order_date": (base_date + timedelta(days=i)).strftime("%Y-%m-%d"),
            "amount": round(10 + i * 1.5, 2),
            "status": valid_statuses[i % len(valid_statuses)],
        }
        rows.append(row)

    # 2. Introduce 3 rows with null customer_name
    #    (set to empty string to represent null in CSV)
    null_name_indices = [5, 12, 25]  # arbitrary distinct indices < 50
    for idx in null_name_indices:
        rows[idx]["customer_name"] = ""

    # 3. Introduce 2 duplicate order_ids
    #    Make row 30 duplicate order_id of row 10, and row 40 duplicate of row 20
    rows[29]["order_id"] = rows[9]["order_id"]
    rows[39]["order_id"] = rows[19]["order_id"]

    # 4. Introduce 2 rows with negative amounts
    negative_amount_indices = [3, 33]
    for idx in negative_amount_indices:
        rows[idx]["amount"] = -abs(rows[idx]["amount"])

    # 5. Introduce 1 row with invalid email (no @ symbol)
    invalid_email_index = 7
    rows[invalid_email_index]["email"] = "invalid.email.example.com"

    # 6. Introduce 1 row with a future date
    future_date_index = 15
    future_date = datetime.now() + timedelta(days=365)
    rows[future_date_index]["order_date"] = future_date.strftime("%Y-%m-%d")

    # 7. Introduce 1 row with status not in (pending, completed, cancelled)
    invalid_status_index = 22
    rows[invalid_status_index]["status"] = "in_progress"

    # Write to CSV
    with open(OUTPUT_FILE, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV file '{OUTPUT_FILE}' created with 50 rows.")

if __name__ == "__main__":
    main()
