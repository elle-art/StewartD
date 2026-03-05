from utils.exceptions import InvalidDataError, MissingFieldError # used in validate_sales_record()
from datetime import datetime # used to add timestamp to errors found in validate_all_records()

def validate_sales_record(record: dict) -> dict:
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
    for key, val in record.items():
        if val == '':
            raise MissingFieldError(f"Value at {key} is empty. Ensure there is a value in each column.")
    # Validate date
    try:
        datetime.strptime(record["date"], "%Y-%m-%d")
    except ValueError:
        raise InvalidDataError("Date must be in YYYY-MM-DD format.")
    # Validate the quantity as a positive entry
    if not isinstance(record["price"], float):
        record["quantity"] = convert_value(record["quantity"])
    if isinstance(record["quantity"], str):
        raise InvalidDataError("Quantity must be a number.")
    if int(record["quantity"]) <= 0:
        raise InvalidDataError("Quantity must be a positive integer.")
    # Validate price as a positive number
    if not isinstance(record["price"], float):
        record["price"] = convert_value(record["price"])
        
    return record

def validate_all_records(records: list) -> tuple[list, list]:
    """
    Validate all records, collecting errors instead of stopping.
    
    Returns: Tuple of (valid_records, error_list)
    """
    valid_records = []
    error_list = []
    for i, record in enumerate(records):
        try: 
            record = validate_sales_record(record) # Validate a single record
        except Exception as e:
            error_entry = {**record, "line_number": i, "timestamp": datetime.now().isoformat(), "error": str(e)}
            error_list.append(error_entry) # If unsuccessful, add to error_list
        else:
            valid_records.append(record) # Successful, add to valid_records
    
    return (valid_records, error_list)

def convert_value(value: str):
    """
    Helper function to convert number types in a record.

    Args:
        value (str): value to be converted

    Returns:
        _type_: the value as an int, float, or None
    """
    value = value.strip()

    # int
    if value.isdigit():
        return int(value)

    # float
    try:
        return float(value)
    except ValueError:
        pass

    # empty → None
    if value == "":
        return None

    return value
