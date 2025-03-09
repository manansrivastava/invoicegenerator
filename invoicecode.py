from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import qrcode
import csv
import os

# Function to Generate QR Code for Payment
def generate_qr_code(invoice_number, total_amount):
    qr = qrcode.make(f"Invoice: {invoice_number}\nAmount: Rs. {total_amount:.2f}")
    qr_path = f"qr_code_{invoice_number}.png"
    qr.save(qr_path)
    return qr_path

# Function to Store Customer Details in CSV
def save_customer_details(customer_name, customer_email, invoice_number, date):
    file_exists = os.path.isfile("customers.csv")
    with open("customers.csv", "a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Customer Name", "Customer Email", "Invoice Number", "Date"])
        writer.writerow([customer_name, customer_email, invoice_number, date])

# Function to Get Invoice Data from User
def get_invoice_data(company_details=None):
    if not company_details:
        print("\n--- Enter Company (Seller) Details ---")
        company_name = input("Company Name: ")
        company_address = input("Company Address: ")
        company_phone = input("Company Phone: ")
        company_email = input("Company Email: ")
        company_details = {
            "company_name": company_name,
            "company_address": company_address,
            "company_phone": company_phone,
            "company_email": company_email
        }
    
    print("\n--- Enter Customer Details ---")
    customer_name = input("Customer Name: ")
    customer_email = input("Customer Email (optional): ")

    invoice_number = "INV-" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    items = []
    while True:
        item_name = input("Enter item name (or type 'done' to finish): ")
        if item_name.lower() == 'done':
            break
        quantity = int(input("Enter quantity: "))
        price = float(input("Enter price per item: "))
        items.append({"name": item_name, "quantity": quantity, "price": price})

    tax_percent = float(input("Enter GST (%) to be applied: "))

    save_customer_details(customer_name, customer_email, invoice_number, date)

    return {
        "invoice_number": invoice_number,
        "date": date,
        **company_details,
        "customer_name": customer_name,
        "customer_email": customer_email,
        "items": items,
        "tax_percent": tax_percent
    }, company_details

# Function to Generate Invoice as PDF
def generate_invoice(filename, invoice_data):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 50, "INVOICE")

    # Company Details
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"{invoice_data['company_name']}")
    c.drawString(50, height - 115, f"{invoice_data['company_address']}")
    c.drawString(50, height - 130, f"Phone: {invoice_data['company_phone']}")
    c.drawString(50, height - 145, f"Email: {invoice_data['company_email']}")

    # Invoice Details
    c.drawString(350, height - 100, f"Invoice No: {invoice_data['invoice_number']}")
    c.drawString(350, height - 115, f"Date: {invoice_data['date']}")
    c.drawString(350, height - 130, f"Customer: {invoice_data['customer_name']}")

    # Table Header
    y = height - 180
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(250, y, "Quantity")
    c.drawString(350, y, "Price (Rs.)")
    c.drawString(450, y, "Total (Rs.)")

    # Items
    c.setFont("Helvetica", 12)
    total_price = 0
    for item in invoice_data["items"]:
        y -= 20
        item_total = item["quantity"] * item["price"]
        c.drawString(50, y, item["name"])
        c.drawString(250, y, str(item["quantity"]))
        c.drawString(350, y, f"Rs. {item['price']:.2f}")
        c.drawString(450, y, f"Rs. {item_total:.2f}")
        total_price += item_total

    # Tax Calculation
    y -= 40
    tax_amount = (total_price * invoice_data["tax_percent"]) / 100
    grand_total = total_price + tax_amount

    c.setFont("Helvetica-Bold", 12)
    c.drawString(350, y, "Subtotal:")
    c.drawString(450, y, f"Rs. {total_price:.2f}")

    y -= 20
    c.drawString(350, y, f"GST ({invoice_data['tax_percent']}%):")
    c.drawString(450, y, f"Rs. {tax_amount:.2f}")

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(350, y, "Grand Total:")
    c.drawString(450, y, f"Rs. {grand_total:.2f}")

    # Generate QR Code for Payment
    qr_path = generate_qr_code(invoice_data["invoice_number"], grand_total)
    c.drawImage(qr_path, 50, y - 100, width=100, height=100)

    c.save()
    print(f"Invoice saved as {filename}")

invoice_count = 1
company_details = None
while True:
    invoice_data, company_details = get_invoice_data(company_details)
    filename = f"invoice{invoice_count}.pdf"
    generate_invoice(filename, invoice_data)
    invoice_count += 1
    more = input("Do you want to create another invoice? (yes/no): ")
    if more.lower() != 'yes':
        break
