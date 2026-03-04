
def calculate_totals(records: list) -> list:
    """
    Calculate line totals (quantity * price) for each record.
    Returns: Records with added 'total' field
    """
    for record in records: 
        record["total"] = record["quantity"] * record["price"]
        

def aggregate_by_store(records) -> dict:
    """
    Aggregate sales by store_id.
    Returns: Dict mapping store_id to total sales
    """
    store_ids = get_unique_vals(records, "store_id") # might have to convert to list
    totals_per_store = {}
    for store in store_ids:
        store_total = 0
        for record in records:
            if record["store_id"] == store:
                store_total += record["price"]
                
        totals_per_store[store] = store_total
            
    return totals_per_store

def aggregate_by_product(records):
    """
    Aggregate sales by product.
    Returns: Dict mapping product to total quantity sold
    """
    inventory = get_unique_vals(records, "product") # might have to convert to list
    totals_per_product = {}
    for product in inventory:
        product_total = 0
        for record in records:
            if record["product"] == product:
                product_total += record["price"]
                
        totals_per_product[product] = product_total
    
    return totals_per_product

def get_unique_vals(records: list, field: str) -> set:
    """helper function that create a set of all store_id in records

    Args:
        records (list): list of dictionary objects

    Returns:
        set: unique store_id values as set
    """
    my_list = []
    for record in records:
        my_list.append(record[field])
    
    return set(my_list)
