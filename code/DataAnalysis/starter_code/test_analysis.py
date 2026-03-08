import pytest
import pandas as pd
from analysis import *

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    return pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North'],
        'total_amt': [20.00, 25.00, 30.00]
    })
    
def test_explore_data_results(sample_data):
    expected = print("""
    Shape:  (3, 9)

Data types:
order_id                 int64
customer_id                str
order_date      datetime64[us]
product_name               str
category                   str
quantity                 int64
unit_price             float64
region                     str
total_amt              float64
dtype: object

Missing values:
order_id        0
customer_id     0
order_date      0
product_name    0
category        0
quantity        0
unit_price      0
region          0
total_amt       0
dtype: int64

Basic numeric stats:
       order_id           order_date  quantity  unit_price  total_amt
count       3.0                    3       3.0    3.000000        3.0
mean        2.0  2024-01-01 16:00:00       2.0   15.000000       25.0
min         1.0  2024-01-01 00:00:00       1.0   10.000000       20.0
25%         1.5  2024-01-01 12:00:00       1.5   10.000000       22.5
50%         2.0  2024-01-02 00:00:00       2.0   10.000000       25.0
75%         2.5  2024-01-02 00:00:00       2.5   17.500000       27.5
max         3.0  2024-01-02 00:00:00       3.0   25.000000       30.0
std         1.0                  NaN       1.0    8.660254        5.0

Date range:
Start: 2024-01-01 00:00:00
End:   2024-01-02 00:00:00
    """)

    actual = explore_data(clean_data(sample_data))
    assert actual == expected

def test_clean_data_removes_duplicates(sample_data):
    """Test that clean_data removes duplicate rows."""
    pd.concat([sample_data, sample_data.loc[[1]]], ignore_index=True)
    expected = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North'],
        'total_amt': [20.00, 25.00, 30.00]
    })

    actual = clean_data(sample_data)
    pd.testing.assert_frame_equal(actual, expected)

def test_sales_by_category_calculation(sample_data):
    """Test that category totals are calculated correctly."""
    expected = pd.DataFrame({
        'category': ['Electronics'],
        'total_sales': [75.00],
        'order_count': [3],
        'avg_order_value': [25.00],
    }).sort_values(by='total_sales', ascending=False)

    actual = sales_by_category(clean_data(sample_data))
    pd.testing.assert_frame_equal(actual, expected)

def test_sales_by_region_calculations(sample_data):
    expected = pd.DataFrame({
        'region': ['North', 'South'],
        'total_sales': [50.00, 25.00],
        'percentage_of_total': [66.67, 33.33],
    })

    actual = sales_by_region(clean_data(sample_data))

    try:
        pd.testing.assert_frame_equal(actual, expected)
    except AssertionError as e:
        print(e, '\n')
        raise DataFrameMismatch(actual, expected)
    except ValueError as e:
        print(e)

def test_top_products_returns_correct_count(sample_data):
    """Test that top_products returns requested number of items."""
    expected = pd.DataFrame({
        'product_name': ['Widget', 'Gadget'],
        'category': ['Electronics', 'Electronics'],
        'total_sales': [50.00, 25.00],
        'quantity': [5, 1],
    })

    actual = top_products(clean_data(sample_data))

    try:
        pd.testing.assert_frame_equal(actual, expected)
    except AssertionError as e:
        print(e, '\n')
        raise DataFrameMismatch(actual, expected)
    except ValueError as e:
        print(e)

def test_daily_sales_trend_calculations(sample_data):
    expected = pd.DataFrame({
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02']),
        'total_sales': [20.00, 55.00],
        'order_count': [1, 2],
    })

    actual = daily_sales_trend(clean_data(sample_data))

    try:
        pd.testing.assert_frame_equal(actual, expected)
    except AssertionError as e:
        print(e, '\n')
        raise DataFrameMismatch(actual, expected)
    except ValueError as e:
        print(e)

def test_customer_analysis_calculations(sample_data):
    expected = pd.DataFrame({
        'customer_id': ['C001', 'C002'],
        'total_spent': [50.00, 25.00],
        'order_count': [2, 1],
        'avg_order_value': [25.00, 25.00],
        'favorite_category': ['Electronics', 'Electronics']
    })

    actual = customer_analysis(clean_data(sample_data))

    try:
        pd.testing.assert_frame_equal(actual, expected)
    except AssertionError as e:
        print(e, '\n')
        raise DataFrameMismatch(actual, expected)
    except ValueError as e:
        print(e)
        
def test_time_features_added(sample_data):
    expected = pd.DataFrame({
        'order_id': [1, 2, 3],
        'customer_id': ['C001', 'C002', 'C001'],
        'order_date': pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-02']),
        'product_name': ['Widget', 'Gadget', 'Widget'],
        'category': ['Electronics', 'Electronics', 'Electronics'],
        'quantity': [2, 1, 3],
        'unit_price': [10.00, 25.00, 10.00],
        'region': ['North', 'South', 'North'],
        'total_amt': [20.00, 25.00, 30.00],
        'day_of_week': [0, 1, 1],
        'month': [1, 1, 1],
        'quarter': [1, 1, 1],
        'is_weekend': [False, False, False],
    })
    expected['day_of_week'] = expected['day_of_week'].astype('int32')
    expected['month'] = expected['month'].astype('int32')
    expected['quarter'] = expected['quarter'].astype('int32')

    actual = add_time_features(clean_data(sample_data))

    try:
        pd.testing.assert_frame_equal(actual, expected)
    except AssertionError as e:
        print(e, '\n')
        raise DataFrameMismatch(actual, expected)
    except ValueError as e:
        print(e)

def test_weekend_vs_weekday_calculations(sample_data):
    expected = {
        "weekend_total_sales": 0.00,
        "weekday_total_sales": 75.00,
        "weekend_percentage": 0.00,
        "weekday_percentage": 100.00,
    }

    actual = weekend_vs_weekday(clean_data(sample_data))

    assert actual == expected

class DataFrameMismatch(AssertionError):
    """Raised when DataFrame shapes are not the same."""
    def __init__(self, actual, expected):
        print('actual', actual)
        print('expected', expected)