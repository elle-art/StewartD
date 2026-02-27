# contact_book.py - Contact Book Application
# Starter code for e003-exercise-data-structures

"""
Contact Book Application
------------------------
A simple contact management system using Python data structures.

Data Structure:
- Each contact is a dictionary with: name, phone, email, category, created_at
- All contacts are stored in a list

Complete the TODO sections below to finish the application.
"""

from datetime import datetime
import time

# =============================================================================
# Initialize Contact Book
# =============================================================================
contacts = []


# =============================================================================
# TODO: Task 1 - Create the Contact Book
# =============================================================================

def add_contact(contacts, name, phone, email, category):
    """
    Add a new contact to the contact book.
    
    Args:
        contacts: The list of all contacts
        name: Contact's full name
        phone: Contact's phone number
        email: Contact's email address
        category: One of: friend, family, work, other
    
    Returns:
        The created contact dictionary
    """
    # TODO: Create a contact dictionary with all fields
    new_contact = {
        "name": name,
        "phone": phone,
        "email": email,
        "category": category
    }
    
    # TODO: Add created_at timestamp using datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_contact["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # TODO: Append to contacts list
    contacts.append(new_contact)
    
    # TODO: Return the new contact
    return new_contact


# =============================================================================
# TODO: Task 2 - Display Contacts
# =============================================================================

def display_all_contacts(contacts):
    """
    Display all contacts in a formatted table.
    
    Output format:
    =============================================
                CONTACT BOOK (X contacts)
    =============================================
    #  | Name            | Phone         | Category
    ---|-----------------|---------------|----------
    1  | Alice Johnson   | 555-123-4567  | friend
    ...
    """
    # TODO: Print header with contact count
    print()
    print("=" * 44)
    print("       CONTACT BOOK (" + str(len(contacts)) + " contacts)")
    print("=" * 44)
    
    # TODO: Print table headers
    print(" #  | Name            | Phone         | Category")
    print(" ---|-----------------|---------------|----------")

    # TODO: Loop through contacts and print each row
    # STUDY THIS ----------------------------------------------------------!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for i, contact in enumerate(contacts, start = 1):
        print(        
            f" {str(i).ljust(3)}| "
            f"{contact['name'].ljust(16)}| "
            f"{contact['phone'].ljust(13)}| "
            f"{contact['category']}"
            f"{contact['created_at']}"
        )
    # TODO: Print footer
    print("=" * 50)



def display_contact_details(contact):
    """
    Display detailed information for a single contact.
    
    Output format:
    --- Contact Details ---
    Name:     [name]
    Phone:    [phone]
    Email:    [email]
    Category: [category]
    Added:    [created_at]
    ------------------------
    """
    # TODO: Print formatted contact details
    print("--- Contact Details ---")
    print("Name:     " + contact["name"])
    print("Phone:    " + contact["phone"])
    print("Email:    " + contact["email"])
    print("Category: " + contact["category"])
    print("Added:    " + contact["created_at"])
    print("------------------------")


# =============================================================================
# TODO: Task 3 - Search Functionality
# =============================================================================

def search_by_name(contacts, query):
    """
    Find contacts whose name contains the query string.
    Case-insensitive search.
    
    Returns:
        List of matching contacts
    """
    # TODO: Filter contacts where query is in name (case-insensitive)
    # Hint: Use list comprehension and .lower()
    return [contact for contact in contacts if query.lower() in contact["name"].lower()]


def filter_by_category(contacts, category):
    """
    Return all contacts in a specific category.
    
    Returns:
        List of contacts matching the category
    """
    # TODO: Filter contacts by category
    return [contact for contact in contacts if category.lower() == contact["category"].lower()]


def find_by_phone(contacts, phone):
    """
    Find a contact by exact phone number.
    
    Returns:
        The contact dictionary if found, None otherwise
    """
    # TODO: Search for contact with matching phone
    for contact in contacts:
        if phone == contact["phone"]:
            return contact
        
    return None # number not found in contact book



# =============================================================================
# TODO: Task 4 - Update and Delete
# =============================================================================

def update_contact(contacts, phone, field, new_value):
    """
    Update a specific field of a contact.
    
    Args:
        contacts: The list of all contacts
        phone: Phone number to identify the contact
        field: The field to update (name, phone, email, or category)
        new_value: The new value for the field
    
    Returns:
        True if updated, False if contact not found
    """
    # TODO: Find contact by phone
    contact = find_by_phone(contacts, phone)
    
    if contact is None:
        return False
    
    # TODO: Update the specified field
    for contact in contacts:
        if phone == contact["phone"]:
            contact[field] = new_value
            return True
    
    # TODO: Return success/failure
    return True


def delete_contact(contacts, phone):
    """
    Delete a contact by phone number.
    
    Returns:
        True if deleted, False if not found
    """
    # TODO: Find and remove contact with matching phone
    # Find contact by phone
    contact = find_by_phone(contacts, phone)
    
    if contact is None:
        return False
    
    # TODO: Update the specified field
    for i, contact in enumerate(contacts, start = 0):
        if phone == contact["phone"]:
            contacts.pop(i)
            return True
    
    # TODO: Return success/failure
    return True


# =============================================================================
# TODO: Task 5 - Statistics
# =============================================================================

def display_statistics(contacts):
    """
    Display statistics about the contact book.
    
    Output:
    --- Contact Book Statistics ---
    Total Contacts: X
    By Category:
      - Friends: X
      - Family: X
      - Work: X
      - Other: X
    Most Recent: [name] (added [date])
    -------------------------------
    """
    
    print("--- Contact Book Statistics ---")
    # TODO: Count total contacts
    print("Total Contacts: " + str(len(contacts)))
    # TODO: Count contacts by category
    friend_ct = 0
    fam_ct = 0
    work_ct = 0
    other_ct = 0
    
    for contact in contacts:
        if contact["category"] == "friend":
            friend_ct += 1
        if contact["category"] == "family":
            fam_ct += 1
        if contact["category"] == "work":
            work_ct += 1
        if contact["category"] == "other":
            other_ct += 1
    
    print("By Category:")
    print(f"  - Friends: {friend_ct}")
    print(f"  - Family: {fam_ct}")
    print(f"  - Work: {work_ct}")
    print(f"  - Other: {other_ct}")
    
    # TODO: Find most recently added contact
    most_recent = contacts[0]
    for x in range(1, len(contacts)):
        if contacts[x]["created_at"] > contacts[x - 1]["created_at"]:
            most_recent = contacts[x]
    print(f"    Most Recent: {most_recent['name']} (added {most_recent['created_at']})")
    print("-------------------------------")


# =============================================================================
# STRETCH GOAL: Interactive Menu
# =============================================================================

def display_menu():
    """Display the main menu."""
    print("\n========== CONTACT BOOK ==========")
    print("1. View all contacts")
    print("2. Add new contact")
    print("3. Search contacts")
    print("4. Update contact")
    print("5. Delete contact")
    print("6. View statistics")
    print("0. Exit")
    print("==================================")


def main():
    """Main function with interactive menu."""
    contacts = []
    # TODO: Implement menu loop
    # Use while True and break on exit choice
    while True: 
        display_menu()
        user_input = input("Select an option 1-6. Use 0 to exit")
        
        if user_input == "1":
            display_all_contacts(contacts)
        if user_input == "2":
            # add_contact(contacts, name, phone, email, category)
            pass
        if user_input == "3":
            # search_by_name(contacts, query)
            # filter_by_category(contacts, category)
            # find_by_phone(contacts, phone)
            pass
        if user_input == "4":
            # update_contact(contacts, phone, field, new_value)
            pass
        if user_input == "5":
            # delete_contact(contacts, phone)
            pass
        if user_input == "6":
            display_statistics(contacts)
        if user_input == "0":
            break


# =============================================================================
# Test Code - Add sample data and test functions
# =============================================================================

if __name__ == "__main__":
    print("Contact Book Application")
    print("=" * 40)
    
    # TODO: Add at least 5 sample contacts
    add_contact(contacts, "Alice Johnson", "555-123-4567", "alice@example.com", "friend")
    add_contact(contacts, "Bob Duncan", "777-123-3210", "bobd@example.com", "friend")
    add_contact(contacts, "Joe Mama", "444-246-8642", "mama@example.com", "family")
    add_contact(contacts, "Sam Smith", "111-111-1111", "ssmith@example.com", "work")
    add_contact(contacts, "Ben Franklin", "000-010-1010", "thebenf@example.com", "other")
    
    # TODO: Test your functions
    # display_all_contacts(contacts) # - DONE
    # display_contact_details(contacts[0]) # - DONE
    # print(search_by_name(contacts, "b")) # - DONE
    # print(filter_by_category(contacts, 'friend')) # - DONE
    # print(find_by_phone(contacts, "111-111-1111")) # - DONE
    # print(find_by_phone(contacts, "111-181-1111")) # - DONE
    # print(update_contact(contacts, "111-111-1111", 'email', "sammyyyyyyyyy@aol.com")) # - DONE
    # display_contact_details(contacts[3])
    # print(update_contact(contacts, "111-181-1111", 'email', "sammyyyyyyyyy@aol.com")) # - DONE
    # delete_contact(contacts, "111-111-1111") # - DONE
    # display_all_contacts(contacts) # - DONE
    # display_statistics(contacts) # - DONE
    # time.sleep(3)
    # add_contact(contacts, "Newest", "111-111-1111", "ssmith@example.com", "work")
    # display_all_contacts(contacts) # - DONE
    # display_statistics(contacts)
    # etc.
    
    
    # STRETCH: Uncomment to run interactive menu
    # main()
