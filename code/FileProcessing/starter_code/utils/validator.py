from FileProcessing.starter_code.utils.exceptions import InvalidDataError, MissingFieldError # used in validate_sales_record()
from datetime import datetime # used to add timestamp to errors found in validate_all_records()

def validate_sales_record(record: dict, line_number: int) -> dict:
    """
    Validate a single sales record.
    
    Required fields: date, store_id, product, quantity, price
    Validation rules:
    - date must be in YYYY-MM-DD format
    - quantity must be a positive integer
    - price must be a positive number
    
    Returns: Validated record with converted types
    Raises: InvalidDataError or MissingFieldError
    """
    TOTAL_REQUIRED_FIELDS = 5
    # Validate all fields are filled out
    if len(record) != TOTAL_REQUIRED_FIELDS:
        raise MissingFieldError(f"Error MISSING_FIELD: missing field. Ensure there is a value in each column (date, store_id, product, quantity, price).\nFound in: {record}")
    # Validate date
    if not datetime.strptime(record["date"], "%Y-%m-%d"):
        raise InvalidDataError(f"Error INVALID_DATA: Date must be in YYYY-MM-DD format.\nFound in {record}")
    # Validate the quantity as a positive entry
    if record["quantity"] <= 0:
        raise InvalidDataError(f"Error INVALID_DATA: Quantity must be a positive integer.\nFound in {record}")
    if not isinstance(record["quantity"], int):
        raise InvalidDataError(f"Error INVALID_DATA: Quantity must be type.\nFound in {record}")
    # Validate price as a positive number
    if not isinstance(record["price"], (int, float)):
        raise InvalidDataError(f"Error INVALID_DATA: Price must be an int or float value.\nFound in {record}")

def validate_all_records(records: list) -> tuple[list, list]:
    """
    Validate all records, collecting errors instead of stopping.
    
    Returns: Tuple of (valid_records, error_list)
    """
    valid_records = []
    error_list = []
    for record in records:
        try: 
            validate_sales_record(record) # Validate a single record
        except:
            record["timestamp"] = datetime.now().isoformat()
            error_list.append(record) # If unsuccessful, add to error_list
        else:
            valid_records.append(record) # Successful, add to valid_records
    
    return (valid_records, error_list)