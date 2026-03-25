# Exercise: Prompt Engineering Lab

## Exercise ID: e021

## Overview

In this hands-on lab, you will practice prompt engineering techniques learned today. You will work through progressively complex challenges, applying zero-shot, few-shot, and chain-of-thought prompting patterns to solve data engineering tasks.

## Learning Objectives

- Apply zero-shot prompting for simple, well-defined tasks
- Use few-shot prompting to teach the model domain-specific patterns
- Implement chain-of-thought prompting for multi-step reasoning
- Apply prompt constraints to control output quality

## Prerequisites

- Access to an LLM (ChatGPT, Claude, Gemini, or similar)
- Completed Monday written content on prompt engineering

## Time Estimate

45-60 minutes

---

## Part 1: Zero-Shot Prompting (15 minutes)

### Challenge 1.1: SQL Generation

Using only zero-shot prompting (no examples), write a prompt that generates a BigQuery SQL query to:

- Find the top 5 departments by average salary
- Include the department name, average salary, and employee count
- Only include departments with more than 10 employees
- Order by average salary descending

**Your Task:**

1. Write your prompt
2. Submit it to the LLM
3. Evaluate the output -- does it produce valid BigQuery SQL?
4. If not, refine your prompt and try again
5. Document your original prompt, your refined prompt (if needed), and the final output
---
### Solution
Original prompt: You are a BigQuery expert. Write me a BigQuery SQL query to retrieve the top 5 departments from the department table, ordering by the average salary descending. Include the department_name, avg_salary, and employee_ct. Ignore departments with an employee_ct less than or equal to 10.

       Returned: COUNT(*) for employee_ct when the count should be stored as a field of the departments table. Would not make sense for a department to show up multiple time in departments.

Refined prompt: You are a BigQuery expert. Write me a BigQuery SQL query to retrieve the top 5 departments from the department table. The fields of the department table are: department_name, avg_salary, and employee_ct. Return these fields. Exclude departments with an employee_ct less than or equal to 10. Order results by the avg_salary descending.

#### Output - Copilot: 

Here’s the clean, direct BigQuery query for your updated schema — no joins, no extra assumptions, just operating on the fields exactly as they exist in the `department` table:

```sql
SELECT
department_name,
avg_salary,
employee_ct
FROM
`your_dataset.department`
WHERE
employee_ct > 10
ORDER BY
avg_salary DESC
LIMIT 5;
```

### Why this is the correct pattern
- Since **avg_salary** and **employee_ct** are already stored fields, there’s **no need for aggregation or GROUP BY**.
- The filter belongs in a **WHERE** clause because you’re filtering on a stored column, not an aggregate.
- Ordering by **avg_salary DESC** gives you the highest‑paying departments first.
- **LIMIT 5** returns the top five.

If you want a version that handles ties, or if your real schema stores salaries in a related table, I can adjust it.
---

### Challenge 1.2: Error Explanation

Write a zero-shot prompt that asks the LLM to explain this error message in plain English and suggest a fix:

```
google.api_core.exceptions.BadRequest: 400 Syntax error: 
Expected end of input but got keyword SELECT at [3:1]
```

**Your Task:**

1. Craft a prompt that provides enough context for a useful explanation
2. Evaluate whether the explanation is accurate
3. Rate the quality of the fix suggestion (1-5 scale)

---
### Solution
My prompt: Explain this error message in plain English: google.api_core.exceptions.BadRequest: 400 Syntax error: 
Expected end of input but got keyword SELECT at [3:1]

### Output - Copilot: 
Here’s the plain‑English meaning of that BigQuery error:

---

## **💡 Simple Explanation**
**BigQuery is telling you that your SQL query should have ended, but instead it found another `SELECT` keyword starting on line 3.**  
In other words, the query has extra text after it should have been finished, or the structure is incomplete or malformed. 

---

## 🧠 What This Usually Means
You likely have one of these issues:

### **1. A stray or misplaced `SELECT`**
- Maybe you accidentally wrote two `SELECT` statements back‑to‑back.
- Or you started a subquery but didn’t wrap it in parentheses.

### **2. A missing keyword before the next `SELECT`**
For example:
- Missing `UNION`, `UNION ALL`, `EXCEPT`, or `INTERSECT`
- Missing `FROM` or closing parentheses

### **3. A copy‑paste fragment left at the bottom of the query**
BigQuery reaches the end of what *should* be a complete query, then sees another `SELECT` and says:  
**“I wasn’t expecting anything else here.”**

---

## 🔍 Example of What Causes This
```sql
SELECT name
FROM my_table
SELECT age   -- ❌ BigQuery hits this and throws the error
```

BigQuery expected the query to end after line 2.

---

## ✅ How to Fix It
- Look at **line 3, column 1** (the `[3:1]` in the error).  
- Remove or fix the unexpected `SELECT`.
- If it’s supposed to be part of a second query, run it separately or combine with `UNION` etc.

---

If you want, paste your query here and I’ll point out the exact spot causing the error.

Rating: 4
Evaluation: With little to no context the syntax of a BiqQuery error is understood by the LLM. It knows there is unexpected syntax around the 'SELECT' keyword in line 3, column 1 of a BigQuery query statement. If specific context of the lines where this error occurred was provided to the LLM, it would likely accurately distinguish which of the 3 possible issues exists. 
---

### Challenge 1.3: Data Dictionary Entry

Write a zero-shot prompt to generate a data dictionary entry for a column called `customer_lifetime_value` in a `dim_customer` table. The entry should include: data type, description, business definition, calculation method, and example values.

**Your Task:**

1. Write the prompt
2. Evaluate whether the output would be useful for a new team member
3. Note what additional context you would need to add to make it more accurate

---
### Solution
My prompt: I have a table called 'dim_customer'. Please make a python data dictionary entry for the column 'customer_lifetime_value' with fields data type, description, business definition, calculation method. Use example value for fields.

### Output:
Here’s a clean, professional **Python-style data dictionary entry** for the `customer_lifetime_value` column in your `dim_customer` table. I’m giving you something that reads like the rest of your pipeline—concise, business‑ready, and actually useful for analysts and engineers.

```python
data_dictionary = {
"customer_lifetime_value": {
       "data_type": "FLOAT64",
       "description": "Total expected revenue a customer will generate over their entire relationship with the business.",
       "business_definition": (
       "A forward-looking metric estimating the net value a customer contributes "
       "across all historical and projected purchases. Used for segmentation, "
       "marketing spend optimization, and customer retention strategies."
       ),
       "calculation_method": (
       "Calculated as the sum of all historical revenue for the customer plus "
       "predicted future revenue based on purchase frequency, average order value, "
       "and churn probability. Example formula: "
       "CLV = (avg_order_value * purchase_frequency / churn_rate)."
       ),
       "example_value": 842.75
}
}
```

If you want, I can also generate entries for the rest of your `dim_customer` columns so you end up with a full, consistent data dictionary for the entire dimension.

Evaluation: This would not be very helpful to a new team member. While the format clear and readable, the information is not accurate. Particularly noticeable in the calculation_method, the provided formula does not match the description. For better accuracy, the LLM would need the true description for the customer_lifetime_value fields. It may be able to infer the types if the whole schema and usage was provided, but it would be best for the developers interacting the system to provide the details.

## Part 2: Few-Shot Prompting (15 minutes)

### Challenge 2.1: Column Name Standardization

You need the LLM to convert column names from various formats to snake_case following your team's convention.

**Provide these examples in your prompt:**

- `CustomerFirstName` -> `customer_first_name`
- `order-total-amount` -> `order_total_amount`
- `PRODUCT ID` -> `product_id`

**Then ask it to convert:**

- `ShippingAddress Line1`
- `total_Revenue_YTD`
- `customerEmailAddress`
- `ORDER__STATUS__CODE`

**Your Task:**

1. Write the few-shot prompt with the 3 examples
2. Submit and evaluate: did it follow the pattern correctly for all 4 inputs?
       - yes, it followed the pattern correctly, everything was lower case and words were seperated by underscores
3. Were there any the model struggled with? Why?
       - ChatGPT, unlike Claude and Gemini, did not provide any explanation for how the conversions worked
       - This is likely because it is designed to retrieve results rather than educate. It also might be personalized to myself and assume that I already know snake_case

### Challenge 2.2: SQL to Documentation

Teach the model to generate documentation from SQL using examples.

**Provide this example:**

Input:

```sql
SELECT customer_id, COUNT(*) as order_count 
FROM orders GROUP BY customer_id
```

Output:

```
Query: Customer Order Count
Purpose: Counts the total number of orders per customer
Tables Used: orders
Output Columns: customer_id, order_count
Aggregation: COUNT grouped by customer_id
```

**Then ask it to document this query:**

```sql
SELECT p.category, 
       DATE_TRUNC(o.order_date, MONTH) as month,
       SUM(o.quantity * p.unit_price) as revenue,
       COUNT(DISTINCT o.customer_id) as unique_customers
FROM orders o
JOIN products p ON o.product_id = p.product_id
WHERE o.order_date >= '2024-01-01'
GROUP BY 1, 2
ORDER BY 1, 2
```

**Your Task:**

1. Write the prompt with the example
2. Evaluate: did the model follow the documentation format?
       - Claude and ChatGPT models followed the format correctly, while Gemini slightly varied from suggested format
3. Is the documentation accurate?
       - All of the models largely assumed the same thing based of the assumption of what each field meant. I would agree with there interpretations but without more detail, it is difficult to varify whether it is correct.

---

## Part 3: Chain-of-Thought Prompting (15 minutes)

### Challenge 3.1: Cost Estimation

Use chain-of-thought prompting to have the LLM estimate BigQuery costs:

**Scenario:**

- You have a table with 500 million rows, each row is approximately 500 bytes
- You run a query that scans 3 columns (out of 20 total columns)
- The query runs 4 times per day
- BigQuery charges $6.25 per TB scanned
- Assume columnar storage distributes data evenly across columns

**Your Task:**

1. Write a prompt that includes "Think through this step by step"
2. Verify each step of the model's calculation
3. Is the final answer reasonable?
4. Did chain-of-thought improve accuracy compared to a direct question?

Prompt: You are a BiqQuery expert. Help me estimate the costs of this BigQuery execution.
I have a  table with 500 million rows, about 500 bytes per row. My query scans 3 of the total 20 columns and runs 4 times a day. BigQuery charges $6.25 per TB scanned. My data is evenly distributed across columns. Help me calculate the costs and explain the calculation.

Output: **Calculating cost estimate**

I need to estimate the cost for scanning a table with 500M rows and 20 columns. The table size is 250 GB, and scanning 3 columns would be about 37.5 GB per query. BigQuery charges $6.25 per TB, so each query costs about $0.23. Running 4 times a day would cost around $0.94 daily, or $28.13 monthly. There's a free 1 TB/month, but the user gave a price, so I’ll focus on that. I’ll keep it concise but explain the calculation clearly.
Here’s the breakdown step by step.

### 1. Estimate table size

- **Rows:** \(500{,}000{,}000\)  
- **Bytes per row:** \(500\)  

\[
\text{Total size} = 500{,}000{,}000 \times 500 = 250{,}000{,}000{,}000 \text{ bytes} \approx 250 \text{ GB} = 0.25 \text{ TB}
\]

### 2. Adjust for only 3 of 20 columns

You said data is evenly distributed across 20 columns, and you scan 3 of them:

\[
\text{Fraction scanned} = \frac{3}{20} = 0.15
\]

\[
\text{Data scanned per query} = 0.25 \text{ TB} \times 0.15 = 0.0375 \text{ TB} = 37.5 \text{ GB}
\]

### 3. Cost per query

BigQuery on-demand: \(\$6.25\) per TB scanned.

\[
\text{Cost per query} = 0.0375 \times 6.25 = 0.234375 \approx \$0.23
\]

### 4. Daily and monthly cost

- **Runs per day:** 4

\[
\text{Daily TB scanned} = 4 \times 0.0375 = 0.15 \text{ TB}
\]
\[
\text{Daily cost} = 0.15 \times 6.25 = 0.9375 \approx \$0.94
\]

Assuming 30 days:

\[
\text{Monthly TB scanned} = 0.15 \times 30 = 4.5 \text{ TB}
\]
\[
\text{Monthly cost} = 4.5 \times 6.25 = 28.125 \approx \$28.13
\]

### Summary

- **Per query:** ~\$0.23  
- **Per day (4 runs):** ~\$0.94  
- **Per 30‑day month:** ~\$28.13  

That’s your rough BigQuery analysis cost for this pattern, ignoring the free 1 TB/month and any storage or other charges.

Evaluation: This query was accurate and detailed. My original prompt could have been more detailed to specify the prices I was looking for, but regardless the LLM accurately estimated the cost per query, per day, and per month.

### Challenge 3.2: Pipeline Debugging

Use chain-of-thought prompting to diagnose this pipeline issue:

**Scenario:**
An ETL pipeline extracts data from a REST API, transforms it with Python, and loads it into BigQuery. The pipeline ran successfully for 30 days, then suddenly started failing with this error:

```
google.api_core.exceptions.Forbidden: 403 Access Denied: 
BigQuery BigQuery: Permission bigquery.tables.create denied
```

Nothing in the pipeline code changed. The GCP project and service account are the same.

**Your Task:**

1. Write a chain-of-thought prompt asking the LLM to reason through possible causes
2. Evaluate the reasoning: are the steps logical?
3. Which root cause does the model identify as most likely?
4. Do you agree? What would you check first?

---
Output: 
Here’s the thing about that error — **it almost never means your code is broken.**  
A pipeline that ran flawlessly for 30 days and then suddenly throws:

```
403 Access Denied: Permission bigquery.tables.create denied
```

…is a classic symptom of **an external change in the environment**, not your ETL.

Let’s walk through the real-world causes that explain this pattern.

---

# 🔍 Why it worked for 30 days, then stopped

## **1. The service account lost a permission due to IAM policy drift**
This is the **#1 cause** in production.

Someone may have:

- Removed a role from the service account  
- Tightened a custom IAM role  
- Replaced a project-level role with a more restrictive one  
- Applied an organization policy that overrides project IAM  

This often happens silently — security teams rotate roles, apply new least‑privilege policies, or update Terraform.

**Why it appears after 30 days:**  
Because the pipeline only tries to *create* a table when a new partition/date/table is needed. For 29 days it was inserting into existing tables. On day 30, it needed to create a new one — and failed.

---

## **2. A dataset or table was deleted and now must be recreated**
If the target table or partition was removed:

- The pipeline attempts to recreate it  
- BigQuery blocks the creation  
- You get `bigquery.tables.create denied`

This can happen if someone manually cleaned up tables or a retention policy expired them.

---

## **3. A new partition or sharded table was needed**
If your pipeline writes to:

- `mytable_YYYYMMDD`  
- or a partition like `mytable$20240324`

…then on the first day of a new month or new cycle, BigQuery must create a new table/partition.

If the service account no longer has `bigquery.tables.create`, it fails **exactly on that day**.

---

## **4. A service account key was rotated and replaced with one tied to a different identity**
If someone rotated keys and accidentally:

- Used a key from a different service account  
- Or replaced the key with one that has fewer permissions  

…the pipeline still “runs” but BigQuery rejects the create operation.

---

## **5. An org policy started blocking table creation**
Some orgs enforce:

- “Deny table creation outside approved datasets”
- “Deny table creation by service accounts”

These policies can be applied at the **org** or **folder** level and propagate downward.

They often take effect days or weeks after being configured.

---

# 🧠 The key insight

Your pipeline didn’t change.  
**Your permissions did.**

And the failure only appears when the pipeline needs to create something new — a table, a partition, or a sharded table.

---

# ✅ How to confirm the root cause

Check the service account’s roles:

### It must have at least one of:
- **BigQuery Data Editor** (`roles/bigquery.dataEditor`)
- **BigQuery Admin** (`roles/bigquery.admin`)
- A custom role containing:
  - `bigquery.tables.create`
  - `bigquery.tables.update`
  - `bigquery.jobs.create`

### Also check:
- Dataset‑level permissions (dataset ACLs)
- Org policies under:
  - `constraints/bigquery.disableTableCreation`
  - `constraints/bigquery.restrictAuthorizedDatasets`

---

# If you want, I can help you pinpoint the exact cause  
Just tell me:

- Whether your pipeline writes to partitioned or sharded tables  
- Whether the table already existed before the failure  
- Whether IAM is managed manually or via Terraform/IaC  

I can help you narrow it down fast.

Evaluation: THe LLM did a good job identifying the possible causes for the error. I agree that the most likely cause is changes to security permissions. It would need more information to narrow down the exact cause.

## Part 4: Constraint Application (Optional, 10 minutes)

### Challenge 4.1: Constrained Output

Write a prompt that generates a Python function with ALL of these constraints:

- Function name: `validate_order_data`
- Input: pandas DataFrame
- Must check for: null values, negative amounts, future dates, duplicate IDs
- Output: a dictionary with check results
- Maximum 30 lines of code
- Must include type hints
- Must include a docstring
- No external libraries beyond pandas and datetime

**Your Task:**

1. Write the prompt with all constraints
2. Did the model satisfy ALL constraints?
3. Which constraints were hardest for the model to follow?

---

Prompt: You are Python expert. Help me make a function called validate_order_data. It takes a pandas DataFrame as a parameter. The function should check for null values, negative amounts, future dates, and duplicate IDs. The function should return a dictionary with the the check results. Include type hints and docstrings. Do not use more than 30 likes of code or libraries other than pandas and datetime.

Output:
from __future__ import annotations
from datetime import datetime
import pandas as pd

def validate_order_data(df: pd.DataFrame) -> dict:
    """
    Validate order data for common issues.

    Checks performed:
    - Null values in any column
    - Negative numeric values
    - Future dates in 'order_date'
    - Duplicate values in 'order_id'

    Parameters
    ----------
    df : pd.DataFrame
        Input order data.

    Returns
    -------
    dict
        Dictionary summarizing validation results.
    """
    now = datetime.now()
    nulls = df.isnull().any().to_dict()
    negatives = {col: (df[col] < 0).any() for col in df.select_dtypes(include="number")}
    future_dates = df["order_date"].apply(lambda d: d > now).any() if "order_date" in df else False
    duplicate_ids = df["order_id"].duplicated().any() if "order_id" in df else False

    return {
        "null_values": nulls,
        "negative_values": negatives,
        "future_dates": future_dates,
        "duplicate_order_ids": duplicate_ids
    }

Evaluation: It follows most of the constraints. It did not adhere to the limit of libraries, and that might have been my fault for including it in an or statement. The LLM might have done the first part end evaluated the expression as true. The extra library is completely unnecessary, but the rest of what is produced is good. This highlights the importance of you being an expert in what you're asking an AI to generate because while it can be good it won't always be perfect.

## Submission

For each challenge, document:

1. Your prompt (original and refined versions)
2. The LLM's output
3. Your evaluation of the output quality (1-5 scale)
4. What you learned about prompting from that challenge

## Reflection Questions

1. Which prompting technique (zero-shot, few-shot, chain-of-thought) produced the best results for data engineering tasks?
2. What made the biggest difference in output quality: specificity, examples, or constraints?
3. When would you choose each technique in your daily work?
