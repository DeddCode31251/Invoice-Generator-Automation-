from dataclasses import dataclass, field


@dataclass
class InvoiceItem:
    """
    Represents one item/service inside an invoice.
    """

    name: str
    quantity: float
    unit_price: float

    @property
    def total(self):
        """
        Calculate the total price for this item.

        Example:
            quantity = 3
            unit_price = 20

            total = 3 * 20 = 60
        """
        return self.quantity * self.unit_price


@dataclass
class Invoice:
    """
    Represents a complete invoice.
    """

    invoice_number: str
    date: str

    customer_name: str
    customer_email: str

    items: list[InvoiceItem] = field(default_factory=list)

    tax_rate: float = 0
    discount: float = 0

    @property
    def subtotal(self):
        """
        Calculate the subtotal of all invoice items.
        """

        return sum(item.total for item in self.items)

    @property
    def tax(self):
        """
        Calculate the tax amount.

        Example:
            subtotal = 100
            tax_rate = 14

            tax = 100 * 14 / 100
                = 14
        """

        return self.subtotal * (self.tax_rate / 100)

    @property
    def total(self):
        """
        Calculate the final invoice total.

        Total = subtotal + tax - discount
        """

        return self.subtotal + self.tax - self.discount
