# invoicegenerator
This project is a Python-based Invoice Generator that allows users to create professional invoices with automated calculations, customer detail storage, and email functionality. The invoices are saved as PDFs and include a QR code for payment. Users can generate multiple invoices while keeping the company details consistent.

Libraries used: 
(1) reportlab – Generates PDFs for invoices, canvas is used to create the invoice layout.
(2) qrcode – Generates QR codes for invoice payments.
(3) datetime – Assigns a unique invoice number based on the current date and time.
(4) csv – Saves customer details in a CSV file for record-keeping.
(5) smtplib – Sends the invoice via email to the customer.
(6) os – Checks if the customers.csv file exists before appending new data.
