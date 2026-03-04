from exceptions import FileProcessingError # validates proper filepaths
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

        f.write(f"\n--- {timestamp} SUMMARY REPORT ---\n")
        f.write(f"Total Records: {total_records}")
        f.write(f"Total Valid Records: {len(valid_records)}")
        f.write(f"Total Errors: {len(errors)} ")
        for err in errors:
            f.write(f"{err}\n")
        
        f.write(f"Sales by Store: \n{sales_per_store}")
        f.write("Top 5 products")

        for i in range(5):
            f.write(f"{sales_per_product[i]}")

def write_clean_csv(filepath: str, records: list[dict]) -> None:
    """
    Write validated records to a clean CSV file.
    """
    # Checks if .csv is the file extension
    if not filepath.endswith(".csv"):
        raise FileProcessingError(filepath, "CSV file must have a .csv extension")
    
    # Writes to CSV file
    with open(filepath, "w") as f:
        f.write(f"Total Valid Records: {len(records)}")
        for record in records:
            f.write(f"{record}\n ")

def write_error_log(filepath: str, errors: list[dict]) -> None:
    """
    Write processing errors to a log file.
    """
    # Checks if .log is the file extension
    if not filepath.endswith(".log"):
        raise FileProcessingError(filepath, "Log file must have a .log extension")
    
    # Appends to error log file
    with open(filepath, "a") as f:
        timestamp = datetime.now().isoformat()
        f.write(f"\n--- Error batch at {timestamp} ---\n")
        f.write(f"Total Errors: {len(errors)}")
        for err in errors:
            f.write(f"{err}\n")
