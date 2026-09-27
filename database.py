import sqlite3
from pathlib import Path

# DATABASE PATH

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATABASE_PATH = DATA_DIR / "invoices.db"


# INITIALIZE DATABASE


def initialize_database():
    """
    Create the data folder and database tables if they
    don't already exist.
    """

    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    # INVOICES TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            invoice_number TEXT UNIQUE NOT NULL,

            date TEXT NOT NULL,

            customer_name TEXT NOT NULL,

            customer_email TEXT,

            tax_rate REAL NOT NULL DEFAULT 0,

            discount REAL NOT NULL DEFAULT 0,

            subtotal REAL NOT NULL DEFAULT 0,

            tax REAL NOT NULL DEFAULT 0,

            total REAL NOT NULL DEFAULT 0
        )
    """)

    # INVOICE ITEMS TABLE

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            invoice_id INTEGER NOT NULL,

            name TEXT NOT NULL,

            quantity REAL NOT NULL,

            unit_price REAL NOT NULL,

            total REAL NOT NULL,

            FOREIGN KEY (invoice_id)
                REFERENCES invoices(id)
                ON DELETE CASCADE
        )
    """)

    connection.commit()

    connection.close()


# SAVE INVOICE


def save_invoice(invoice):
    """
    Save an invoice and all of its items into SQLite.

    The invoice object can be either:

    1. A dictionary from the current invoice.py
    2. A future Invoice model object
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    try:

        # INSERT INVOICE


        cursor.execute(
            """
            INSERT INTO invoices (
                invoice_number,
                date,
                customer_name,
                customer_email,
                tax_rate,
                discount,
                subtotal,
                tax,
                total
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            (
                invoice["invoice_number"],
                invoice["date"],
                invoice["customer_name"],
                invoice["customer_email"],
                invoice["tax_rate"],
                invoice["discount"],
                invoice["subtotal"],
                invoice["tax"],
                invoice["total"],
            ),
        )

        # Get the ID SQLite assigned to the invoice
        invoice_id = cursor.lastrowid


        # INSERT ITEMS


        for item in invoice["items"]:
            cursor.execute(
                """
                INSERT INTO invoice_items (
                    invoice_id,
                    name,
                    quantity,
                    unit_price,
                    total
                )

                VALUES (?, ?, ?, ?, ?)
            """,
                (
                    invoice_id,
                    item["name"],
                    item["quantity"],
                    item["unit_price"],
                    item["total"],
                ),
            )

        connection.commit()

    except Exception:
        # If something goes wrong, undo the transaction.
        connection.rollback()

        raise

    finally:
        connection.close()


# GET ALL INVOICES


def get_all_invoices():
    """
    Return all saved invoices.

    Results are ordered newest first.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM invoices
        ORDER BY id DESC
    """)

    invoices = cursor.fetchall()

    connection.close()

    return invoices


# GET ONE INVOICE


def get_invoice(invoice_number):
    """
    Get an invoice and all of its items using the
    invoice number.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    # Get invoice
    cursor.execute(
        """
        SELECT *
        FROM invoices
        WHERE invoice_number = ?
    """,
        (invoice_number,),
    )

    invoice = cursor.fetchone()

    if invoice is None:
        connection.close()
        return None

    # Get items
    cursor.execute(
        """
        SELECT *
        FROM invoice_items
        WHERE invoice_id = ?
        ORDER BY id ASC
    """,
        (invoice["id"],),
    )

    items = cursor.fetchall()

    connection.close()

    return {"invoice": invoice, "items": items}


# DELETE INVOICE


def delete_invoice(invoice_number):
    """
    Delete an invoice from the database.
    """

    connection = sqlite3.connect(DATABASE_PATH)

    cursor = connection.cursor()

    try:
        # Find invoice ID
        cursor.execute(
            """
            SELECT id
            FROM invoices
            WHERE invoice_number = ?
        """,
            (invoice_number,),
        )

        result = cursor.fetchone()

        if result is None:
            return False

        invoice_id = result[0]

        # Delete items first
        cursor.execute(
            """
            DELETE FROM invoice_items
            WHERE invoice_id = ?
        """,
            (invoice_id,),
        )

        # Delete invoice
        cursor.execute(
            """
            DELETE FROM invoices
            WHERE id = ?
        """,
            (invoice_id,),
        )

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
