# Exercise: AI Code Review Challenge

## Exercise ID: e024

## Overview

In this exercise, you will review AI-generated code for correctness, security, and best practices. You will act as the senior engineer reviewing pull requests from an "AI junior developer." This exercise builds the critical review skills necessary for production-quality AI-assisted development.

## Learning Objectives

- Review AI-generated code systematically for bugs and vulnerabilities
- Identify common patterns where AI produces incorrect or insecure code
- Apply a structured review checklist to AI output
- Improve AI-generated code to meet production standards

## Prerequisites

- Python 3.10+ knowledge
- SQL/BigQuery knowledge
- Completed Thursday written content on AI testing and debugging

## Time Estimate

45-60 minutes

---

## Part 1: Bug Detection (20 minutes)

Review the following AI-generated code snippets. Each contains at least one bug. Find and fix all bugs.

### Snippet 1: Data Deduplication

The AI was asked: "Write a Python function to deduplicate a DataFrame keeping the most recent record."

```python
def deduplicate_records(df, key_column, date_column):
    """Remove duplicate records, keeping the most recent."""
    df_sorted = df.sort_values(date_column, ascending=True)
    df_deduped = df_sorted.drop_duplicates(subset=key_column, keep='first')
    return df_deduped
```

**Questions:**

1. What bug(s) exist in this code?
ascending=True, shows the earliest dates, not the most recent
2. What is the fix?
set ascending=False
3. What edge cases are not handled?
checking for correct types, null values; if date column has invalid/mismatched types than the sort won't work

### Snippet 2: BigQuery Table Creation

The AI was asked: "Write a function to create a partitioned BigQuery table."

```python
from google.cloud import bigquery

def create_partitioned_table(project_id, dataset_id, table_id):
    client = bigquery.Client(project=project_id)
    
    schema = [
        bigquery.SchemaField("order_id", "INTEGER"),
        bigquery.SchemaField("customer_id", "INTEGER"),
        bigquery.SchemaField("order_date", "DATE"),
        bigquery.SchemaField("amount", "FLOAT"),
    ]
    
    table_ref = f"{project_id}.{dataset_id}.{table_id}"
    table = bigquery.Table(table_ref, schema=schema)
    
    table.time_partitioning = bigquery.TimePartitioning(
        type_=bigquery.TimePartitioningType.DAY,
        field="order_date",
        expiration_ms=7776000000  # 90 days
    )
    
    table = client.create_table(table)
    print(f"Created table {table.table_id}")
    return table
```

**Questions:**

1. Is this code functionally correct?
2. What happens if the table already exists?
an exception will raise
3. What data type issue exists with the `amount` field for financial data?
FLOAT could cause rounding errors, should use NUMERIC for more precision
4. Is `expiration_ms` appropriate for a production fact table? What risks does it create?
no, it risks losing data

### Snippet 3: CSV Processing Pipeline

The AI was asked: "Write a function to process CSV files and load to BigQuery."

```python
import pandas as pd
from google.cloud import bigquery

def process_and_load(file_path, table_id):
    # Read CSV
    df = pd.read_csv(file_path)
    
    # Clean data
    df = df.dropna()
    df['date'] = pd.to_datetime(df['date'])
    df['amount'] = df['amount'].astype(float)
    
    # Load to BigQuery
    client = bigquery.Client()
    job = client.load_table_from_dataframe(df, table_id)
    job.result()
    
    print(f"Loaded {len(df)} rows to {table_id}")
```

**Questions:**

1. What happens if the file does not exist?
FileNotFound error raises
2. What happens if the `date` column contains invalid dates?
An ValueError raises because pd.to_datetime() will not be able to convert an invalid date
3. Is `dropna()` appropriate? What data might be lost?
Yes and no, it would be best to drop only the null values in critical columns. If date is missing, but the amount is valid, the entry should remain
4. What write disposition is used by default? Is this safe?
append by default (client.load_table_from_dataframe(df, table_id)), might enter duplicate data
5. What logging/monitoring is missing?
It's not logging the job.result() or invalid rows of df

---

## Part 2: Security Review (15 minutes)

Review these AI-generated snippets for security issues.

### Snippet 4: Database Connection

```python
import os
from google.cloud import bigquery

def get_client():
    # Service account credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/keys/service-account.json'
    client = bigquery.Client(project='production-project-12345')
    return client

def run_query(query_text):
    client = get_client()
    query = f"SELECT * FROM analytics.customers WHERE name = '{query_text}'"
    results = client.query(query).result()
    return [dict(row) for row in results]
```

**Questions:**

1. Identify ALL security issues in this code
- credentials made public
- project id made public
- sql injection
2. For each issue, explain the risk
You do not want these posted in your repo for hackers to find. Do not put in direct links and do not store credentials in the project.
Without parameterize on query_text, a hacker could retrieve the entire table
3. Rewrite the code with proper security practices
use a .env file and loadenv to get the variables in place of string paths

### Snippet 5: API Key Usage

```python
import requests

OPENAI_API_KEY = "sk-proj-abc123def456ghi789..."

def generate_summary(text):
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": text}]
        }
    )
    return response.json()['choices'][0]['message']['content']
```

**Questions:**

1. What is the primary security issue?
Public API key
2. What happens if this code is committed to a public repository?
Anyone, probably a bot, could gain access to your API
3. Rewrite using secure credential management
put it in an .env

---

## Part 3: Best Practices Review (10 minutes)

### Snippet 6: Data Validation

The AI was asked: "Write data validation for our ETL pipeline."

```python
def validate(df):
    if len(df) == 0:
        return False
    if df.isnull().sum().sum() > 0:
        return False
    for col in df.columns:
        if df[col].dtype == 'object':
            if df[col].str.len().max() > 1000:
                return False
    return True
```

**Questions:**

1. What are the code quality issues?
many a issue, should scrap and try again.
- use df.empty
- don't use sum() in that if statement values().any()
- using string method on all object types will not work
- doesn't validate any numerics
- no error logs, returns boolean
2. The function returns a boolean -- is this sufficient for production use?
No, because you'll want to know which data entries are invalid
3. Rewrite to provide detailed validation results (which checks failed and why)
4. Add proper logging and documentation

---

## Part 4: Improvement Exercise (Optional, 15 minutes)

Take any ONE snippet from above and create a production-ready version:

1. Fix all bugs and security issues
2. Add comprehensive error handling
3. Add logging
4. Add type hints and docstrings
5. Add input validation
6. Write 3 unit tests for the improved code

You may use AI assistance for this task, but you must review every line of the AI's output and justify each acceptance or modification.

```python
def deduplicate_records(df, key_column, date_column):
    """Remove duplicate records, keeping the most recent."""
    df['date_column'] = pd.to_datetime(df['date_column'], errors='raise') # check for invalid dates first

    df_sorted = df.sort_values(date_column, ascending=True)
    df_deduped = df_sorted.drop_duplicates(subset=key_column, keep='first')
    return df_deduped

print(deduplicate_records(my_df, "order_id", "order_date"))
```
---

## Review Checklist (Print and Use)

For each code snippet:

| # | Check | Status |
| - | ----- | ------ |
| 1 | Does it do what was requested? | |
| 2 | Input validation present? | |
| 3 | Error handling present? | |
| 4 | No hardcoded credentials? | |
| 5 | SQL injection prevention? | |
| 6 | Appropriate logging? | |
| 7 | Type hints included? | |
| 8 | Docstrings present? | |
| 9 | Edge cases handled? | |
| 10 | Would pass code review? | |

## Submission

Submit:

1. Your bug findings for each snippet (Part 1)
2. Your security analysis (Part 2)
3. Your best practices review (Part 3)
4. Your improved code (Part 4, if completed)
5. Brief reflection: What patterns did you notice in AI-generated code issues?
