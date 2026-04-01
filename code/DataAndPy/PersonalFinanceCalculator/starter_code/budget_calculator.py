# budget_calculator.py - Personal Finance Calculator
# Starter code for e002-exercise-python-intro

"""
Personal Finance Calculator
---------------------------
This program helps users understand their monthly budget by collecting
income and expense information and displaying a formatted summary.

Complete the TODO sections below to finish the program.
"""

def validate_expense(val):
    if val < 0:
        return 0
    else:
        return val

print("=" * 44)
print("       PERSONAL FINANCE CALCULATOR")
print("=" * 44)
print()

# =============================================================================
# TODO: Task 1 - Collect User Information
# =============================================================================
# Get the user's name
# Example: name = input("Enter your name: ")
name = input("Enter your name: ")

# add value if no name input
if name == "":
    name = "Anonymous"

# Get monthly income (as a float)
# Remember to convert the input to a float!
monthly_income = float(input("Enter monthly income: "))

if monthly_income <= 0:
    print("***** ERROR: Monthly income must be greater than 0 *****")
    exit()

# Get expenses for at least 4 categories:
# - rent: Rent/Housing
# - utilities: Utilities (electric, water, internet)
# - food: Food/Groceries
# - transportation: Transportation (gas, public transit)
rent_cost = validate_expense(float(input("Enter rent amount: ")))
utilities_cost = validate_expense(float(input("Enter utilities amount: ")))
food_cost = validate_expense(float(input("Enter food amount: ")))
transportation_cost = validate_expense(float(input("Enter transportation amount: ")))

# =============================================================================
# TODO: Task 2 - Perform Calculations
# =============================================================================
# Calculate total expenses
expenses = rent_cost + utilities_cost + food_cost + transportation_cost

# Calculate remaining balance (income - expenses)
remaining_bal = monthly_income - expenses

# Calculate savings rate as a percentage
# Formula: (balance / income) * 100
savings_rate = (remaining_bal / monthly_income) * 100

# Determine financial status
# - If balance > 0: status = "in the green"
# - If balance < 0: status = "in the red"
# - If balance == 0: status = "breaking even"
if remaining_bal > 0:
    status = "in the green"
if remaining_bal < 0:
    status = "in the red"
if remaining_bal == 0:
    status == "breaking even"

# =============================================================================
# TODO: Task 3 - Display Results
# =============================================================================
# Create a formatted budget report
# Use f-strings for formatting
# Dollar amounts should show 2 decimal places: f"${amount:.2f}"
# Percentages should show 1 decimal place: f"{rate:.1f}%"

# Example structure:
# print("=" * 44)
# print("       MONTHLY BUDGET REPORT")
# print("=" * 44)
# print(f"Name: {name}")
# ... continue building the report ...
print()
print("=" * 44)
print("       MONTHLY BUDGET REPORT")
print("=" * 44)
print()
print("Name: " + name)
print("Monthly Income: " + "${:.2f}".format(monthly_income))
print()
print("EXPENSES: ")
print("  - Rent/Housing:    " + "${:.2f}".format(rent_cost))
print("  - Utilities:       " + "${:.2f}".format(utilities_cost))
print("  - Food/Groceries:  " + "${:.2f}".format(food_cost))
print("  - Transportation:  " + "${:.2f}".format(transportation_cost))
print("-" * 44)
print("Total Expenses: " + "${:.2f}".format(expenses))
print("Remaining Balance: " + "${:.2f}".format(remaining_bal))
print("Savings Rate: " + f"{savings_rate:.1f}%")
print()
print("EXPENSE BREAKDOWN: ")
print("  - Rent/Housing:    " + f"{((rent_cost / monthly_income) * 100):.1f}%" + " of income")
print("  - Utilities:       " + f"{((utilities_cost / monthly_income) * 100):.1f}%" + " of income")
print("  - Food/Groceries:  " + f"{((food_cost / monthly_income) * 100):.1f}%" + " of income")
print("  - Transportation:  " + f"{((transportation_cost / monthly_income) * 100):.1f}%" + " of income")
print()
print("Status: You are " + status + "!")
print("=" * 44)

# =============================================================================
# TODO: Task 4 - Add Validation (Optional Enhancement)
# =============================================================================
# Add these validations before calculations:
# - If name is empty, use "Anonymous"
# - If income is <= 0, print error and exit
# - If any expense is negative, treat as 0


# =============================================================================
# STRETCH GOAL: Category Percentages
# =============================================================================
# Add a section showing what percentage each expense is of total income
# Example: print(f"  - Rent/Housing:    {(rent/income)*100:.1f}% of income")
