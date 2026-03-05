from utils.file_io.file_reader import read_csv_file
from utils.validator import validate_all_records
from utils.transformer import calculate_totals, aggregate_by_product, aggregate_by_store
from utils.file_io.report_writer import write_summary_report, write_clean_csv, write_error_log

"""
## Definition of Done

- [ ] All custom exceptions are defined
- [ ] File reader handles encoding and missing files
- [ ] Validator catches all error types without crashing
- [ ] Transformer correctly calculates totals and aggregations
- [ ] Reports are generated in proper format
- [ ] Pipeline processes the sample file successfully
- [ ] Errors are logged, not swallowed

---

## Stretch Goals (Optional)

1. Add support for JSON input files
2. Implement a retry mechanism for transient file errors
3. Add a `--verbose` flag for detailed logging
4. Create a context manager for the entire pipeline that cleans up on failure

---

## Submission

1. Ensure all modules are complete and tested
2. Process the sample file and verify outputs
3. Be prepared to demonstrate error handling by introducing bad data
"""
def process_sales_file(input_path, output_dir):
    """
    Main processing pipeline.
    
    1. Read the input file
    2. Validate all records
    3. Transform valid records
    4. Generate reports
    5. Handle any errors gracefully
    
    Returns: ProcessingResult with statistics
    """
    sales_list: list[dict] = read_csv_file(input_path)    # 1. Read the input file
    validated_sales_records, invalid_records = validate_all_records(sales_list)     # 2. Validate all records

    # 3. Transform valid records
    complete_sales_record: list[dict] = calculate_totals(validated_sales_records)   # Adds total costs to each individual records
    sales_by_store_record: list[dict] = aggregate_by_store(validated_sales_records) # Calculates the total amount sold per store
    sales_by_product_record: list[dict] = aggregate_by_product(validated_sales_records)  # Calculates the total amount sold per product
    # 4. Generate reports
    write_summary_report(f"{output_dir}/results.txt", complete_sales_record, invalid_records, (sales_by_store_record, sales_by_product_record))
    write_clean_csv(f"{output_dir}/sales_records.csv", complete_sales_record)
    write_error_log(f"{output_dir}/invalid_data.log", invalid_records)
    #5. Handle any errors gracefully


if __name__ == "__main__":
    # Process from command line
    process_sales_file("utils/sample_sales.csv", "output")
    print("Output successfully created at ./output/") #might need exceptions here