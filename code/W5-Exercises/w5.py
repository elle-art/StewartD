import pandas as pd

my_df = pd.DataFrame({
    "order_id": [1, 1, 1, 2, 3, 3],
    "order_date": [
        "2024-01-01",
        "2024-01-03",   # latest for order_id=1
        "2024-01-02",
        "2024-02-10",   # unique
        "2024-03-05",
        "2024-03-01"    # earlier duplicate for order_id=3
    ],
    "amount": [100, 150, 120, 200, 300, 250]
})

def deduplicate_records(df, key_column, date_column):
    """Remove duplicate records, keeping the most recent."""
    df_sorted = df.sort_values(date_column, ascending=True)
    df_deduped = df_sorted.drop_duplicates(subset=key_column, keep='first')
    return df_deduped

print(deduplicate_records(my_df, "order_id", "order_date"))


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
