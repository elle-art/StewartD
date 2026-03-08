import pandas as pd

# Data Loading and Exploration
def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the orders dataset.
    - Parse dates correctly
    - Handle missing values
    - Return a clean DataFrame
    """
    data_as_dataframe = pd.read_csv(filepath) # Load date from file to dataframe
    clean_data_frame = clean_data(data_as_dataframe) # Cleans data
    
    return clean_data_frame

def explore_data(df: pd.DataFrame) -> None:
    """
    Print basic statistics about the dataset:
    - Shape (rows, columns)
    - Data types
    - Missing value counts
    - Basic statistics for numeric columns
    - Date range covered
    """
    # Shape
    print("Shape: ", df.shape)
    # Data types
    print("\nData types:")
    print(df.dtypes)
    # How many missing vals
    print("\nMissing values:")
    print(df.isna().sum())
    # Numeric stats
    print("\nBasic numeric stats:")
    print(df.describe())
    # Date range
    print("\nDate range:")
    print("Start:", df['order_date'].min())
    print("End:  ", df['order_date'].max())

# Data Cleaning and Transformation
def clean_data(df: pd.DataFrame) -> None:
    """
    Clean the dataset:
    - Remove duplicates
    - Fill or drop missing values (document your strategy)
    - Standardize text columns (strip whitespace, consistent case)
    - Add calculated columns: 'total_amt' = quantity * unit_price
    """
    # Remove duplicate entries
    df.drop_duplicates()
    # Fill in missing values with None
    df.fillna("None")
    # Standardize text - rm whitespace, upper, lower
    df = df.apply(lambda col: col.str.strip() if col.dtype == "object" else col) # strips whitespace
    # Converts text values to title case
    text_cols = ["region", "category", "product_name"]   
    df[text_cols] = df[text_cols].apply(lambda col: col.str.title())
    # Converts number values to int and float
    df["quantity"]  = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)

    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce").fillna(0).astype(float)

    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce") # Converts date values to datetime
    df["total_amt"] = df["quantity"] * df["unit_price"] # Calculates total and adds col to df
    return df
    
def add_time_features(df):
    """
    Add time-based features:
    - day_of_week (0=Monday, 6=Sunday)
    - month
    - quarter
    - is_weekend (boolean)
    """
    df['day_of_week'] = df['order_date'].dt.dayofweek
    df['month'] = df['order_date'].dt.month
    df['quarter'] = df['order_date'].dt.quarter
    df['is_weekend'] = df['day_of_week'] >= 5

    return df

# Analysis Functions
def sales_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total sales and order count by category.
    Returns: DataFrame with columns [category, total_sales, order_count, avg_order_value]
    Sorted by total_sales descending.
    """
    cat_data = df.groupby('category').agg(
        total_sales=('total_amt', 'sum'),
        order_count=('total_amt', 'count'),
        avg_order_value=('total_amt', 'mean')
    ).reset_index() # aggregates data and ensures 'category' is a column instead of an index

    return cat_data[['category', 'total_sales', 'order_count', 'avg_order_value']].sort_values(by='total_sales', ascending=False) # sorts desc 

def sales_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate total sales by region.
    Returns: DataFrame with columns [region, total_sales, percentage_of_total]
    """
    total_sales = df['total_amt'].sum()
    
    regional_data = df.groupby('region').agg(
        total_sales=('total_amt', 'sum')
        ).assign(
            percentage_of_total=lambda x: round(((x['total_sales'] / total_sales) * 100), 2)
        ).reset_index()
    
    return regional_data[['region', 'total_sales', 'percentage_of_total']]

def top_products(df: pd.DataFrame, n: int=10) -> pd.DataFrame:
    """
    Find top N products by total sales.
    Returns: DataFrame with columns [product_name, category, total_sales, quantity]
    """
    product_date = df.groupby('product_name').agg(category=('category', 'first'),total_sales=('total_amt', 'sum'), quantity=('quantity', 'sum')).reset_index()
    
    return product_date.nlargest(n, 'total_sales').reset_index(drop=True)

def daily_sales_trend(df):
    """
    Calculate daily sales totals.
    Returns: DataFrame with columns [order_date, total_sales, order_count]
    """
    daily_data = df.groupby('order_date').agg(
        total_sales=('total_amt', 'sum'),
        order_count=('total_amt', 'count')).reset_index()
    
    return daily_data[['order_date', 'total_sales', 'order_count']].sort_values('order_date')

def customer_analysis(df):
    """
    Analyze customer purchasing behavior.
    Returns: DataFrame with columns [customer_id, total_spent, order_count, 
            avg_order_value, favorite_category]
    """
    counts = df.groupby(['customer_id', 'category']).size()
    favorite = counts.groupby('customer_id').idxmax().str[1].astype(str)# test these to see difference
    
    customer_data = df.groupby('customer_id').agg(
        total_spent=('total_amt', 'sum'),
        order_count=('total_amt', 'count'),
        avg_order_value=('total_amt', 'mean')).assign(
        favorite_category=favorite).reset_index()
    
    return customer_data[['customer_id', 'total_spent', 'order_count', 'avg_order_value', 'favorite_category']]

def weekend_vs_weekday(df: pd.DataFrame) -> dict:
    """
    Compare weekend vs weekday sales.
    Returns: Dict with weekend and weekday total sales and percentages.
    """
    total= df['total_amt'].sum()
    df = add_time_features(df)

    day_data = df.groupby('is_weekend').agg(
        total_sales=('total_amt', 'sum')
        ).assign(
            percentage_of_total=lambda x: round(((x['total_sales'] / total) * 100), 2)
        )
    
    # NOTE: When you use .groupby() the columns you pass become an index, not a column. This is why .loc[idx1, idx2] works below
    # NOTE: if needed to prevent error if there are no T/F values     
    weekend_total = float(day_data.loc[True, "total_sales"]) if True in day_data.index else 0.0
    weekday_total = float(day_data.loc[False, "total_sales"]) if False in day_data.index else 0.0

    weekend_pct = float(day_data.loc[True, "percentage_of_total"]) if True in day_data.index else 0.0
    weekday_pct = float(day_data.loc[False, "percentage_of_total"]) if False in day_data.index else 0.0

    return {
        "weekend_total_sales": weekend_total,
        "weekday_total_sales": weekday_total,
        "weekend_percentage": weekend_pct,
        "weekday_percentage": weekday_pct,
    }



