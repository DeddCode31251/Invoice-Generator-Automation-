from datetime import datetime


def create_invoice(customer_name, customer_email, items, tax_rate, discount):
    invoice_number = f"INV-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    subtotal = 0

    # Calculate each item's total
    for item in items:
        item["total"] = item["quantity"] * item["unit_price"]
        subtotal += item["total"]

    # Calculate tax
    tax = subtotal * (tax_rate / 100)

    # Calculate final amount
    total = subtotal + tax - discount

    return {
        "invoice_number": invoice_number,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "customer_name": customer_name,
        "customer_email": customer_email,
        "items": items,
        "subtotal": subtotal,
        "tax_rate": tax_rate,
        "tax": tax,
        "discount": discount,
        "total": total,
    }
