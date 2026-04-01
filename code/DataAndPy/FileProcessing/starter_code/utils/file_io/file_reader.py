import logging
"""
Requirements:

- Use context managers (`with` statement)
- Log errors before re-raising
- Return empty list for empty files (not an error)

"""

def read_csv_file(filepath: str) -> list[dict]:
    """
    Read a CSV file and return a list of dictionaries.
    
    Should handle:
    - FileNotFoundError
    - UnicodeDecodeError (try utf-8, then latin-1)
    - Empty files
    
    Returns: List of dictionaries (one per row)
    Raises: FileProcessingError with descriptive message
    """
    records = [] # List of dictionaries
    try:
        try: 
            with open(filepath, "r", encoding="utf-8") as f:
                records = parse_to_list(f, records)
        except UnicodeDecodeError:
            with open(filepath, "r", encoding="latin-1") as f:
                records = parse_to_list(f, records)
    except FileNotFoundError as e:
        logging.error("File not found at %s: %s", filepath, e)
        raise  
    
    return records


def parse_to_list(f, records_list) -> list[dict]:
    """Helper function to parse .csv lines into a list of dictionary objects.

    Args:
        f (TextIOWrapper): file to be parsed

    Returns:
        list[dict]: a list of dictionary object represented .csv records
    """
    # Read file line by line
    for i, line in enumerate(f):
        if i == 0: # Get columns form first line of .csv
            keys = [column for column in line.strip().split(",")]
            if keys == []: # If first line empty, assume file empty and return an empty list
                return []
        else:     
            # Parse an entry line to a dictionary obj    
            entry = line.strip().split(",")
            entry_as_dict = {}
            for x, key in enumerate(keys):
                entry_as_dict[key] = entry[x]
        
            records_list.append(entry_as_dict) # Add new dictionary to records
    
    return records_list

