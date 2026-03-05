from ..exceptions import FileProcessingError # validates proper filepaths
from datetime import datetime # used to add timestamp to reports


def write_summary_report(filepath: str, valid_records: list[dict], errors: list[dict], aggregations: tuple) -> None:
    """
    Write a formatted summary report.
    
    Report should include:
    - Processing timestamp
    - Total records processed
    - Number of valid records
    - Number of errors (with details)
    - Sales by store
    - Top 5 products
    """
    total_records = len(valid_records) + len(errors)
    sales_per_store, sales_per_product = aggregations
    
    # Checks if .txt or .md is the file extension
    if not filepath.endswith(".txt") and not filepath.endswith(".md"):
        raise FileProcessingError(filepath, "Report file must have a .txt or .md extension")
    
    # Writes to report file
    with open(filepath, "w") as f:
        timestamp = datetime.now().isoformat()

        f.write(f"=== Sales Processing Report ===\n")
        f.write(
        f"""
Generated: {timestamp}
        
Processing Statistics:
- Total records: {total_records}
- Valid records: {len(valid_records)}
- Error records: {len(errors)}
        """)
        f.write(f"\nErrors:\n")
        for err in errors:
            f.write(f"- Line {err["line_number"]}: {err["error"]}\n")
        f.write(f"\nSales by Store:\n")
        for store, total in sales_per_store.items():
            f.write(f"- {store}: {total}\n")
        f.write("\nTop Products:\n")
        for i, (product, quantity) in enumerate(sales_per_product.items()):
            f.write(f"{i + 1}. {product}: {quantity} units\n")

def write_clean_csv(filepath: str, records: list[dict]) -> None:
    """
    Write validated records to a clean CSV file.
    """
    added_col_headers = False
    # Checks if .csv is the file extension
    if not filepath.endswith(".csv"):
        raise FileProcessingError(filepath, "CSV file must have a .csv extension")
    
    # Writes to CSV file
    with open(filepath, "w") as f:
        for record in records:
            csv_str = ''
            for key, val in record.items():
                if not added_col_headers: 
                    f.write(f"{key},")                    
                csv_str += (f"{val},")
            f.write(f"\n")
            added_col_headers = True # Makes flag True after keys have been printed
            f.write(f"{csv_str}")

def write_error_log(filepath: str, errors: list[dict]) -> None:
    """
    Write processing errors to a log file.
    """
    # Checks if .log is the file extension
    if not filepath.endswith(".log"):
        raise FileProcessingError(filepath, "Log file must have a .log extension")
    
    # Appends to error log file
    with open(filepath, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"\n--- Error batch at {timestamp} ---\n")
        f.write(f"Total Errors: {len(errors)}\n")
        for err in errors:
            f.write(f"{err}\n")
