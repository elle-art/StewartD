"""
4. Generates all visualizations
5. Prints a summary report to console

-----------

## Definition of Done

- [ ] Data loads and cleans without errors
- [ ] All analysis functions return correct results
- [ ] At least 4 visualizations are created
- [ ] Dashboard displays all key metrics
- [ ] Main script runs end-to-end


---
"""
from DataAndPy.DataAnalysis.starter_code.analysis import *
from DataAndPy.DataAnalysis.starter_code.visualizations import *

def main(input_path, output_dir):
    data = load_data(input_path)
    explore_data(data)
    
    category = sales_by_category(data)
    region = sales_by_region(data)
    products = top_products(data)
    daily = daily_sales_trend(data)
    customer = customer_analysis(data)
    week = weekend_vs_weekday(data)

    create_category_bar_chart(category, f"{output_dir}/category.png")
    create_regional_pie_chart(region, f"{output_dir}/region.png")
    create_sales_trend_line(daily, f"{output_dir}/daily.png")
    create_dashboard(f"{output_dir}")

if __name__ == "__main__":
    # Process from command line
    main("utils/orders.csv", "output")
    print("Output successfully created at ./output/") #might need exceptions here