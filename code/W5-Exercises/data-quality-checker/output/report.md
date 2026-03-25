# Data Quality Report

**Generated**: 2026-03-25 17:24:23 UTC
**File**: sample_data.csv
**Total Rows**: 50

## Summary

| Check | Status | Issues Found |
| ----- | ------ | ------------ |
| Null Values | WARNING | 3 |
| Duplicates | FAIL | 4 |
| Negative Values | WARNING | 2 |
| Future Dates | WARNING | 1 |
| Email Format | WARNING | 1 |

**Total Issues**: 11

## Detailed Results

### Null Values
- Status: **WARNING**
- Issues Found: **3**
- Recommendation: No nulls detected.
- Null details by column:
  - order_id: 0 nulls (0.0%)
  - customer_name: 3 nulls (6.0%)
  - email: 0 nulls (0.0%)
  - order_date: 0 nulls (0.0%)
  - amount: 0 nulls (0.0%)
  - status: 0 nulls (0.0%)

### Duplicates
- Status: **FAIL**
- Issues Found: **4**
- Recommendation: Remove duplicate rows or collapse them with aggregation.
- Duplicate indices: [9, 19, 29, 39]
- Duplicate values: ['ORD0010', 'ORD0020']

### Negative Values
- Status: **WARNING**
- Issues Found: **2**
- Recommendation: No invalid negative values found.
  - amount: 2 negative (4.0%), indices [3, 33]

### Future Dates
- Status: **WARNING**
- Issues Found: **1**
- Recommendation: Check date source and adjust future values where not plausible.
- Future indices: [15]
- Future values: ['2027-03-25T00:00:00']

### Email Format
- Status: **WARNING**
- Issues Found: **1**
- Recommendation: Normalize or validate emails; fix malformed entries.
- Invalid indices: [7]
- Invalid values: ['invalid.email.example.com']
