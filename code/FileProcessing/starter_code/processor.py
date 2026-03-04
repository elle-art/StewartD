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
    pass

if __name__ == "__main__":
    # Process from command line
    process_sales_file("sample_sales.csv", "/output/results.txt")
    print("Output successfully created at /output/results.txt") #might need exceptions here