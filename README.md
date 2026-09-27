# Invoice Generator

A Python-based invoice management application that allows you to create invoices, calculate totals, store invoice data in SQLite, and generate professional PDF invoices.

The project is designed as a practical Python application with separate modules for invoice calculations, database management, PDF generation, and the command-line interface.

---

## Features

* Create new invoices
* Add multiple products or services to an invoice
* Calculate item totals automatically
* Calculate invoice subtotal
* Calculate tax
* Apply discounts
* Calculate the final invoice total
* Generate unique invoice numbers
* Save invoices to a SQLite database
* Store invoice items separately from invoice information
* View previously saved invoices
* List invoice history
* Delete invoices
* Generate PDF invoices
* Automatically create required directories
* Input validation for numbers and required fields
* Command-line interface

---

## Project Structure

```text
invoice-generator/
│
├── main.py
├── invoice.py
├── models.py
├── database.py
├── pdf_generator.py
│
├── data/
│   └── invoices.db
│
└── invoices/
    ├── INV-0001.pdf
    ├── INV-0002.pdf
    └── ...
```

---

## File Responsibilities

### `main.py`

The main entry point of the application.

It handles:

* Application startup
* Database initialization
* User input
* Main menu
* Creating invoices
* Listing invoices
* Viewing invoices
* Deleting invoices

---

### `invoice.py`

Contains the invoice calculation logic.

It handles:

* Creating invoice data
* Generating invoice numbers
* Calculating item totals
* Calculating subtotal
* Calculating tax
* Calculating discounts
* Calculating the final total

Example:

```python
subtotal = 500

tax = subtotal * (14 / 100)

total = subtotal + tax - discount
```

---

### `models.py`

Contains the data models used by the application.

The project uses Python `dataclasses` to represent:

* Invoice items
* Invoices

Example:

```python
InvoiceItem(
    name="Website",
    quantity=1,
    unit_price=500
)
```

An invoice can contain multiple `InvoiceItem` objects.

---

### `database.py`

Handles SQLite database operations.

It is responsible for:

* Creating the database
* Creating database tables
* Saving invoices
* Saving invoice items
* Retrieving invoices
* Listing invoices
* Deleting invoices

The database is stored at:

```text
data/invoices.db
```

---

### `pdf_generator.py`

Handles PDF generation using ReportLab.

It creates PDF invoices containing:

* Invoice number
* Date
* Customer information
* Invoice items
* Quantities
* Unit prices
* Item totals
* Subtotal
* Tax
* Discount
* Final total

Generated PDFs are stored in:

```text
invoices/
```

---

# How the Application Works

The application follows a simple flow:

```text
                    ┌───────────────┐
                    │    main.py    │
                    │  User Input   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  invoice.py   │
                    │ Calculations  │
                    └───────┬───────┘
                            │
                 ┌──────────┴──────────┐
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌──────────────────┐
        │   database.py   │   │ pdf_generator.py │
        │     SQLite      │   │      PDF         │
        └────────┬────────┘   └────────┬─────────┘
                 │                     │
                 ▼                     ▼
        ┌─────────────────┐   ┌──────────────────┐
        │ data/invoices.db│   │ invoices/*.pdf   │
        └─────────────────┘   └──────────────────┘
```

---

# Requirements

You need:

* Python 3.10 or newer
* pip
* ReportLab

SQLite is included with Python, so no separate SQLite installation is required.

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/invoice-generator.git
```

Move into the project:

```bash
cd invoice-generator
```

---

## 2. Create a virtual environment

Linux/macOS:

```bash
python3 -m venv venv
```

Windows:

```powershell
python -m venv venv
```

---

## 3. Activate the virtual environment

### Linux/macOS

```bash
source venv/bin/activate
```

### Windows

```powershell
venv\Scripts\activate
```

---

## 4. Install dependencies

```bash
pip install reportlab
```

---

# Running the Application

Run:

```bash
python main.py
```

On Linux systems where `python` points to Python 2 or is unavailable:

```bash
python3 main.py
```

You should see:

```text
============================================================
                   INVOICE GENERATOR
============================================================

1. Create new invoice
2. List invoices
3. View invoice
4. Delete invoice
5. Exit

Choose an option:
```

---

# Creating an Invoice

Select:

```text
1. Create new invoice
```

The application asks for customer information:

```text
Customer name: John Smith
Customer email: john@example.com
```

Then you can add products or services:

```text
--- Invoice Items ---

Add Item

Item/service name: Website Development
Quantity: 1
Unit price: 500

Add another item? (y/n): y

Add Item

Item/service name: Hosting
Quantity: 1
Unit price: 50

Add another item? (y/n): n
```

Then enter the tax and discount:

```text
Tax (%): 14
Discount: 20
```

The application calculates the invoice automatically.

---

# Invoice Calculation

Suppose an invoice contains:

```text
Website Development
Quantity: 1
Unit Price: $500

Hosting
Quantity: 1
Unit Price: $50
```

The item totals are:

```text
Website Development = 1 × $500 = $500

Hosting = 1 × $50 = $50
```

The subtotal becomes:

```text
Subtotal = $500 + $50

Subtotal = $550
```

If the tax rate is 14%:

```text
Tax = $550 × 14 / 100

Tax = $77
```

If the discount is $20:

```text
Total = Subtotal + Tax - Discount

Total = $550 + $77 - $20

Total = $607
```

The invoice will therefore contain:

```text
Subtotal:       $550.00
Tax:             $77.00
Discount:        $20.00
-----------------------
TOTAL:          $607.00
```

---

# Database

The project uses SQLite.

The database file is:

```text
data/invoices.db
```

SQLite is useful for this project because it is:

* Lightweight
* Built into Python
* Serverless
* Easy to deploy
* Stored as a single file
* Suitable for a small local application

---

# Database Structure

The application uses two main tables.

## `invoices`

Stores general invoice information.

```text
invoices
│
├── id
├── invoice_number
├── date
├── customer_name
├── customer_email
├── tax_rate
├── discount
├── subtotal
├── tax
└── total
```

---

## `invoice_items`

Stores the individual items belonging to an invoice.

```text
invoice_items
│
├── id
├── invoice_id
├── name
├── quantity
├── unit_price
└── total
```

The relationship looks like:

```text
invoices
   │
   │ 1
   │
   │
   │ many
   ▼
invoice_items
```

One invoice can contain many invoice items.

For example:

```text
Invoice INV-0001
│
├── Website
├── Hosting
├── Domain
└── Maintenance
```

---

# PDF Generation

PDF files are generated using the `reportlab` package.

Generated invoices are saved inside:

```text
invoices/
```

Example:

```text
invoices/
├── INV-0001.pdf
├── INV-0002.pdf
└── INV-0003.pdf
```

A generated PDF contains information such as:

```text
INVOICE

Invoice Number: INV-0001
Date: 2026-09-27

Customer:
John Smith
john@example.com

-----------------------------------------------
Item / Service       Quantity   Price   Total
-----------------------------------------------
Website                  1       $500    $500
Hosting                  1        $50     $50
-----------------------------------------------

Subtotal:                         $550
Tax (14%):                         $77
Discount:                          $20
-----------------------------------------------
TOTAL:                            $607
```

---

# Invoice Management

The application provides several operations.

## Create Invoice

Creates a new invoice and:

1. Calculates the totals
2. Saves the invoice to SQLite
3. Saves its items
4. Generates a PDF

---

## List Invoices

Displays previously created invoices.

Example:

```text
Invoice           Date           Customer                Total
-----------------------------------------------------------------
INV-0003          2026-09-27     Sarah                    $450.00
INV-0002          2026-09-26     Ahmed                    $720.00
INV-0001          2026-09-25     John                     $607.00
```

---

## View Invoice

Enter an invoice number:

```text
Invoice number: INV-0001
```

The application retrieves the invoice and its items from SQLite and displays the complete invoice.

---

## Delete Invoice

Enter an invoice number:

```text
Invoice number: INV-0001
```

The application shows the invoice information and asks for confirmation:

```text
Are you sure you want to delete it? (y/n):
```

Enter:

```text
y
```

to delete the invoice.

---

# Input Validation

The application validates user input where appropriate.

For example, entering:

```text
Quantity: abc
```

produces:

```text
Invalid number. Please try again.
```

Required text fields cannot be left empty.

For example:

```text
Customer name:
```

produces:

```text
This field cannot be empty.
```

Negative values are also rejected for values such as:

* Quantity
* Unit price
* Tax
* Discount

---

# Python Concepts Used

This project demonstrates several important Python concepts.

### Functions

The application is divided into functions:

```python
def create_new_invoice():
    ...
```

```python
def list_invoices():
    ...
```

```python
def view_invoice():
    ...
```

---

### Dictionaries

Invoice information can be represented using dictionaries:

```python
invoice = {
    "invoice_number": "INV-0001",
    "customer_name": "John",
    "customer_email": "john@example.com",
    "subtotal": 500,
    "tax": 70,
    "total": 570
}
```

---

### Dataclasses

The project also provides structured models through `models.py`:

```python
@dataclass
class InvoiceItem:
    name: str
    quantity: float
    unit_price: float
```

---

### SQLite

The project uses Python's built-in:

```python
sqlite3
```

module to communicate with the database.

Parameterized queries are used when inserting user data:

```python
cursor.execute(
    """
    INSERT INTO invoices (...)
    VALUES (?, ?, ?, ...)
    """,
    values
)
```

This avoids constructing SQL queries by directly concatenating user input.

---

### File System Management

The project uses:

```python
pathlib.Path
```

to manage directories and files.

Example:

```python
BASE_DIR = Path(__file__).resolve().parent
```

---

### Exception Handling

The application uses:

```python
try:
    ...
except Exception:
    ...
```

to handle errors without unexpectedly terminating the application.

---

# Dependencies

The project currently uses:

```text
reportlab
```

Install it with:

```bash
pip install reportlab
```

Python's standard library provides the other functionality used by the project, including:

```text
sqlite3
datetime
pathlib
dataclasses
typing
```

---

# Example Workflow

A complete invoice creation workflow looks like this:

```text
1. Start application
        │
        ▼
2. Initialize SQLite database
        │
        ▼
3. Select "Create new invoice"
        │
        ▼
4. Enter customer information
        │
        ▼
5. Add invoice items
        │
        ▼
6. Enter tax and discount
        │
        ▼
7. Calculate invoice
        │
        ├───────────────┐
        ▼               ▼
8. Save database     9. Generate PDF
        │               │
        ▼               ▼
invoices.db          INV-0001.pdf
```

---

# Example Project Session

```text
============================================================
                   INVOICE GENERATOR
============================================================

1. Create new invoice
2. List invoices
3. View invoice
4. Delete invoice
5. Exit

Choose an option: 1


============================================================
                    CREATE NEW INVOICE
============================================================

--- Customer Information ---

Customer name: John Smith
Customer email: john@example.com

--- Invoice Items ---

Add Item

Item/service name: Website Development
Quantity: 1
Unit price: 500

Add another item? (y/n): y

Add Item

Item/service name: Hosting
Quantity: 1
Unit price: 50

Add another item? (y/n): n

--- Tax & Discount ---

Tax (%): 14
Discount: 20


============================================================
                        INVOICE
============================================================

Invoice number: INV-0001
Date:           2026-09-27
Customer:       John Smith
Email:          john@example.com

------------------------------------------------------------
ITEMS
------------------------------------------------------------
Website Development              1.00 x $    500.00 = $    500.00
Hosting                          1.00 x $     50.00 = $     50.00

------------------------------------------------------------
Subtotal:                                      $    550.00
Tax (14%):                                     $     77.00
Discount:                                      -$     20.00
------------------------------------------------------------
TOTAL:                                         $    607.00
============================================================

Invoice created successfully!

Invoice number: INV-0001
PDF: invoices/INV-0001.pdf
```

---

# Future Improvements

Possible future versions of the project can add:

## Invoice Features

* Sequential invoice numbering
* Invoice editing
* Duplicate invoice
* Invoice search
* Invoice filtering
* Invoice status
* Due dates
* Payment status
* Notes
* Terms and conditions

## Customer Management

* Customer database
* Customer history
* Customer search
* Customer addresses
* Customer phone numbers
* Customer company names

## Business Information

* Company name
* Company logo
* Company address
* Phone number
* Email
* Website
* Tax registration number

## Currency

Support for multiple currencies:

```text
USD
EUR
GBP
EGP
SAR
AED
```

## PDF Improvements

* Company logo
* Custom colors
* Better typography
* Professional invoice templates
* Page numbers
* Payment instructions
* QR codes
* Bank information
* Signature area

## Application Improvements

* Graphical user interface
* Web interface
* REST API
* User authentication
* Multiple businesses
* Cloud database
* Online invoice sharing
* Email invoices to customers

---

# Planned Architecture

A larger version of the application could eventually look like:

```text
invoice-generator/
│
├── app/
│   │
│   ├── models/
│   │   ├── invoice.py
│   │   ├── customer.py
│   │   └── item.py
│   │
│   ├── services/
│   │   ├── invoice_service.py
│   │   ├── pdf_service.py
│   │   └── customer_service.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   └── repositories.py
│   │
│   └── utils/
│       ├── validators.py
│       └── formatters.py
│
├── data/
│   └── invoices.db
│
├── invoices/
│
├── tests/
│
├── main.py
├── requirements.txt
└── README.md
```

This structure would make it easier to expand the project into a larger application.

---

# Testing

Run the application:

```bash
python main.py
```

Test the following:

### Create

```text
1. Create new invoice
```

Create an invoice containing multiple items.

### List

```text
2. List invoices
```

Verify that the newly created invoice appears.

### View

```text
3. View invoice
```

Enter its invoice number and verify that all information is displayed correctly.

### Delete

```text
4. Delete invoice
```

Delete a test invoice and verify that it no longer appears in the invoice list.

### PDF

Check:

```text
invoices/
```

and verify that the corresponding PDF was generated.

---

# Error Handling

Common issues include:

### ReportLab is not installed

Error:

```text
ModuleNotFoundError: No module named 'reportlab'
```

Install it:

```bash
pip install reportlab
```

---

### Database problems

Delete the existing database:

```text
data/invoices.db
```

Then run the application again.

The application will recreate the database and its tables.

---

# Data Storage

The application stores invoice information locally.

Database:

```text
data/invoices.db
```

Generated documents:

```text
invoices/
```

The SQLite database should be backed up if the invoices are important.

---

# Security Considerations

The application is currently designed as a local application.

If it is later converted into a web application, additional security should be implemented, including:

* Authentication
* Authorization
* Password hashing
* Input validation
* CSRF protection
* Secure session handling
* Database access controls
* File upload validation
* Secure PDF storage
* HTTPS

---

# License

This project can be licensed according to the requirements of the project owner.

For an open-source project, a common option is the MIT License.

---

# Author

Deadcode

Dead
