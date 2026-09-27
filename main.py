from database import (
    delete_invoice,
    get_all_invoices,
    get_invoice,
    initialize_database,
    save_invoice,
)
from invoice import create_invoice
from pdf_generator import generate_invoice_pdf

# DISPLAY FUNCTIONS


def print_header(title):
    """
    Print a formatted section header.
    """

    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60)



# INPUT HELPERS



def get_float(prompt, minimum=None):
    """
    Safely ask the user for a number.

    Example:
        quantity = get_float("Quantity: ", minimum=0)
    """

    while True:
        try:
            value = float(input(prompt))

            if minimum is not None and value < minimum:
                print(f"Please enter a value >= {minimum}.")
                continue

            return value

        except ValueError:
            print("Invalid number. Please try again.")


def get_non_empty_input(prompt):
    """
    Ask the user for text and make sure it isn't empty.
    """

    while True:
        value = input(prompt).strip()

        if value:
            return value

        print("This field cannot be empty.")



# CREATE INVOICE



def create_new_invoice():
    """
    Create a new invoice.

    Steps:

        1. Get customer information
        2. Get invoice items
        3. Get tax and discount
        4. Create invoice
        5. Save invoice
        6. Generate PDF
        7. Display invoice
    """

    print_header("CREATE NEW INVOICE")

    # CUSTOMER INFORMATION

    print("\n--- Customer Information ---")

    customer_name = get_non_empty_input("Customer name: ")

    customer_email = input("Customer email: ").strip()

    # INVOICE ITEMS

    print("\n--- Invoice Items ---")

    items = []

    while True:
        print("\nAdd Item")

        item_name = get_non_empty_input("Item/service name: ")

        quantity = get_float("Quantity: ", minimum=0)

        unit_price = get_float("Unit price: ", minimum=0)

        item = {"name": item_name, "quantity": quantity, "unit_price": unit_price}

        items.append(item)

        another = input("\nAdd another item? (y/n): ").strip().lower()

        if another != "y":
            break

    # TAX AND DISCOUNT

    print("\n--- Tax & Discount ---")

    tax_rate = get_float("Tax (%): ", minimum=0)

    discount = get_float("Discount: ", minimum=0)

    # CREATE INVOICE

    invoice = create_invoice(
        customer_name=customer_name,
        customer_email=customer_email,
        items=items,
        tax_rate=tax_rate,
        discount=discount,
    )

    # SAVE TO DATABASE

    try:
        save_invoice(invoice)

    except Exception as error:
        print("\nERROR: Could not save invoice.")
        print(f"Details: {error}")

        return

    # GENERATE PDF

    try:
        pdf_path = generate_invoice_pdf(invoice)

    except Exception as error:
        print("\nWARNING: Invoice was saved, but PDF generation failed.")
        print(f"Details: {error}")

        pdf_path = None

    # DISPLAY RESULT

    display_invoice(invoice)

    print("\n" + "=" * 60)

    print("Invoice created successfully!")

    print(f"Invoice number: {invoice['invoice_number']}")

    if pdf_path:
        print(f"PDF: {pdf_path}")

    print("=" * 60)



# DISPLAY INVOICE



def display_invoice(invoice):
    """
    Display a complete invoice in the terminal.

    Works with the dictionary returned by invoice.py.
    """

    print("\n" + "=" * 60)
    print("INVOICE".center(60))
    print("=" * 60)

    print(f"Invoice number: {invoice['invoice_number']}")

    print(f"Date:           {invoice['date']}")

    print(f"Customer:       {invoice['customer_name']}")

    print(f"Email:          {invoice['customer_email']}")

    print("\n" + "-" * 60)

    print("ITEMS")
    print("-" * 60)

    for item in invoice["items"]:
        print(
            f"{item['name']:<25}"
            f"{item['quantity']:>8.2f} x "
            f"${item['unit_price']:>10.2f}"
            f" = ${item['total']:>10.2f}"
        )

    print("-" * 60)

    print(f"{'Subtotal:':<45}${invoice['subtotal']:>10.2f}")

    print(f"{'Tax (' + str(invoice['tax_rate']) + '%):':<45}${invoice['tax']:>10.2f}")

    print(f"{'Discount:':<45}-${invoice['discount']:>9.2f}")

    print("-" * 60)

    print(f"{'TOTAL:':<45}${invoice['total']:>10.2f}")

    print("=" * 60)



# LIST INVOICES



def list_invoices():
    """
    Display all invoices stored in the database.
    """

    print_header("INVOICE HISTORY")

    invoices = get_all_invoices()

    if not invoices:
        print("\nNo invoices found.")
        return

    print()

    print(f"{'Invoice':<18}{'Date':<15}{'Customer':<20}{'Total':>10}")

    print("-" * 65)

    for invoice in invoices:
        print(
            f"{invoice['invoice_number']:<18}"
            f"{invoice['date']:<15}"
            f"{invoice['customer_name'][:19]:<20}"
            f"${invoice['total']:>9.2f}"
        )



# VIEW INVOICE



def view_invoice():
    """
    Find an invoice by invoice number and display it.
    """

    print_header("VIEW INVOICE")

    invoice_number = input("\nInvoice number: ").strip()

    if not invoice_number:
        print("Invoice number cannot be empty.")
        return

    result = get_invoice(invoice_number)

    if result is None:
        print(f"\nInvoice '{invoice_number}' was not found.")

        return

    invoice_data = result["invoice"]
    items_data = result["items"]

    # Convert database rows back into the structure
    # expected by display_invoice()

    invoice = {
        "invoice_number": invoice_data["invoice_number"],
        "date": invoice_data["date"],
        "customer_name": invoice_data["customer_name"],
        "customer_email": invoice_data["customer_email"],
        "tax_rate": invoice_data["tax_rate"],
        "discount": invoice_data["discount"],
        "subtotal": invoice_data["subtotal"],
        "tax": invoice_data["tax"],
        "total": invoice_data["total"],
        "items": [],
    }

    for item in items_data:
        invoice["items"].append(
            {
                "name": item["name"],
                "quantity": item["quantity"],
                "unit_price": item["unit_price"],
                "total": item["total"],
            }
        )

    display_invoice(invoice)



# DELETE INVOICE



def remove_invoice():
    """
    Delete an invoice from the database.
    """

    print_header("DELETE INVOICE")

    invoice_number = input("\nInvoice number: ").strip()

    if not invoice_number:
        print("Invoice number cannot be empty.")
        return

    # Check whether invoice exists first

    result = get_invoice(invoice_number)

    if result is None:
        print(f"\nInvoice '{invoice_number}' was not found.")

        return

    invoice = result["invoice"]

    print("\nInvoice found:")
    print(f"Customer: {invoice['customer_name']}")
    print(f"Total:    ${invoice['total']:.2f}")

    confirmation = (
        input("\nAre you sure you want to delete it? (y/n): ").strip().lower()
    )

    if confirmation != "y":
        print("\nDeletion cancelled.")
        return

    deleted = delete_invoice(invoice_number)

    if deleted:
        print(f"\nInvoice '{invoice_number}' deleted successfully.")

    else:
        print("\nCould not delete invoice.")



# MAIN MENU



def show_menu():
    """
    Display the main application menu.
    """

    print("\n" + "=" * 60)

    print("INVOICE GENERATOR".center(60))

    print("=" * 60)

    print("""
1. Create new invoice
2. List invoices
3. View invoice
4. Delete invoice
5. Exit
""")



# MAIN



def main():
    """
    Main application loop.
    """

    # INITIALIZE DATABASE

    try:
        initialize_database()

    except Exception as error:
        print("ERROR: Could not initialize database.")
        print(f"Details: {error}")

        return

    # APPLICATION LOOP

    while True:
        show_menu()

        choice = input("Choose an option: ").strip()

        # CREATE

        if choice == "1":
            create_new_invoice()

        # LIST

        elif choice == "2":
            list_invoices()

        # VIEW

        elif choice == "3":
            view_invoice()

        # DELETE

        elif choice == "4":
            remove_invoice()

        # EXIT

        elif choice == "5":
            print("\nGoodbye!")
            break

        # INVALID OPTION

        else:
            print("\nInvalid option. Please choose a number from 1 to 5.")



# PROGRAM ENTRY POINT


if __name__ == "__main__":
    main()
