import os
import matplotlib.pyplot as plt
from DataAndPy.DataAnalysis.starter_code.analysis import add_time_features

def create_category_bar_chart(category_data, output_path):
    """
    Create a horizontal bar chart of sales by category.
    - Include value labels on bars
    - Use a professional color scheme
    - Save to output_path
    """
    plt.bar(category_data['category'], category_data['total_sales'])
    plt.savefig(output_path)
    plt.close()


def create_regional_pie_chart(region_data, output_path):
    """
    Create a pie chart showing sales distribution by region.
    - Include percentages
    - Use distinct colors for each region
    - Save to output_path
    """
    values = region_data["total_sales"]
    labels = region_data["region"]

    plt.figure(figsize=(6, 6))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Sales by Region")

    plt.savefig(output_path)
    plt.close()

def create_sales_trend_line(daily_data, output_path):
    """
    Create a line chart showing daily sales trend.
    - Include moving average (7-day)
    - Mark weekends differently
    - Add proper axis labels and title
    - Save to output_path
    """
    # Add 7-day moving average
    daily_data['ma7'] = daily_data['total_sales'].rolling(7).mean()

    # Add weekend flag
    daily_data = add_time_features(daily_data)

    # --- Plotting ---
    plt.figure(figsize=(12, 6))

    # Base daily sales line
    plt.plot(
        daily_data['order_date'],
        daily_data['total_sales'],
        label='Daily Sales',
        color='steelblue',
        linewidth=1.5
    )

    # Moving average line
    plt.plot(
        daily_data['order_date'],
        daily_data['ma7'],
        label='7-Day Moving Average',
        color='darkorange',
        linewidth=2
    )

    # Highlight weekends
    weekend_dates = daily_data[daily_data['is_weekend']]['order_date']
    weekend_sales = daily_data[daily_data['is_weekend']]['total_sales']

    plt.scatter(
        weekend_dates,
        weekend_sales,
        color='red',
        label='Weekend',
        s=40,
        alpha=0.7
    )

    # Labels + title
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    plt.title("Daily Sales Trend with 7-Day Moving Average")
    plt.legend()
    plt.tight_layout()

    # Save figure
    plt.savefig(output_path)
    plt.close()


def create_dashboard(output_dir):
    """
    Create a multi-panel dashboard with 4 subplots:
    1. Sales by category (bar)
    2. Sales by region (pie)
    3. Daily trend (line)
    4. Top 10 products (horizontal bar)
    
    Save as a single figure.
    """
    # Paths to the saved images
    category_path = os.path.join(output_dir, "category.png")
    region_path = os.path.join(output_dir, "region.png")
    trend_path = os.path.join(output_dir, "daily.png")
    # products_path = os.path.join(output_dir, "top_products.png")

    # Load images
    img_category = plt.imread(category_path)
    img_region = plt.imread(region_path)
    img_trend = plt.imread(trend_path)
    # img_products = plt.imread(products_path)

    # Create dashboard figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))

    axes[0, 0].imshow(img_category)
    axes[0, 0].set_title("Sales by Category")
    axes[0, 0].axis("off")

    axes[0, 1].imshow(img_region)
    axes[0, 1].set_title("Sales by Region")
    axes[0, 1].axis("off")

    axes[1, 0].imshow(img_trend)
    axes[1, 0].set_title("Daily Sales Trend")
    axes[1, 0].axis("off")

    # axes[1, 1].imshow(img_products)
    # axes[1, 1].set_title("Top 10 Products")
    # axes[1, 1].axis("off")

    plt.tight_layout()

    dashboard_path = os.path.join(output_dir, "sales_dashboard.png")
    fig.savefig(dashboard_path, dpi=300)
    plt.close(fig)

