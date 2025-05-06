import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime, timedelta

# Function to generate a sample invoice image for testing
def generate_sample_invoice(output_path):
    # Create a blank white image
    width, height = 2100, 2970  # A4 size at 300 DPI
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Try to load fonts
    try:
        header_font = ImageFont.truetype('Arial', 48)
        title_font = ImageFont.truetype('Arial', 36)
        normal_font = ImageFont.truetype('Arial', 24)
    except IOError:
        # Fall back to default font
        header_font = ImageFont.load_default()
        title_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()
    
    # Generate random invoice data
    invoice_number = f"INV-{random.randint(1000, 9999)}"
    
    # Random date in the last 30 days
    invoice_date = datetime.now() - timedelta(days=random.randint(1, 30))
    invoice_date_str = invoice_date.strftime("%m/%d/%Y")
    
    # Due date is 30 days after invoice date
    due_date = invoice_date + timedelta(days=30)
    due_date_str = due_date.strftime("%m/%d/%Y")
    
    # Random vendor name
    vendors = ["TechSupplies Inc.", "Office Solutions Ltd.", "Global Services Corp.", "ProEquip Industries", "SmartBusiness LLC"]
    vendor_name = random.choice(vendors)
    
    # Random items
    items = [
        ("Office Desk Chair", random.randint(1, 5), random.uniform(80, 150)),
        ("Laptop Stand", random.randint(1, 10), random.uniform(25, 60)),
        ("Wireless Mouse", random.randint(1, 20), random.uniform(15, 40)),
        ("USB-C Hub", random.randint(1, 8), random.uniform(30, 80)),
        ("Monitor", random.randint(1, 3), random.uniform(200, 500))
    ]
    
    # Calculate totals
    subtotal = sum(qty * price for _, qty, price in items)
    tax_rate = 0.08  # 8% tax
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount
    
    # Draw invoice header
    draw.text((100, 100), vendor_name, font=header_font, fill='black')
    draw.text((100, 180), "123 Business St., Suite 456", font=normal_font, fill='black')
    draw.text((100, 230), "Anytown, ST 12345", font=normal_font, fill='black')
    draw.text((100, 280), "Phone: (555) 123-4567", font=normal_font, fill='black')
    
    # Draw Invoice title
    draw.text((width - 600, 100), "INVOICE", font=header_font, fill='black')
    
    # Draw invoice details
    y_pos = 400
    draw.text((100, y_pos), f"Invoice #: {invoice_number}", font=title_font, fill='black')
    y_pos += 60
    draw.text((100, y_pos), f"Invoice Date: {invoice_date_str}", font=title_font, fill='black')
    y_pos += 60
    draw.text((100, y_pos), f"Due Date: {due_date_str}", font=title_font, fill='black')
    y_pos += 100
    
    # Draw "Bill To" section
    draw.text((100, y_pos), "Bill To:", font=title_font, fill='black')
    y_pos += 60
    draw.text((100, y_pos), "Sample Customer", font=normal_font, fill='black')
    y_pos += 40
    draw.text((100, y_pos), "456 Client Road", font=normal_font, fill='black')
    y_pos += 40
    draw.text((100, y_pos), "Clientville, ST 54321", font=normal_font, fill='black')
    y_pos += 100
    
    # Draw table header
    col1, col2, col3, col4 = 100, 1000, 1300, 1600
    
    draw.text((col1, y_pos), "Description", font=title_font, fill='black')
    draw.text((col2, y_pos), "Quantity", font=title_font, fill='black')
    draw.text((col3, y_pos), "Unit Price", font=title_font, fill='black')
    draw.text((col4, y_pos), "Amount", font=title_font, fill='black')
    
    y_pos += 50
    draw.line([(100, y_pos), (width - 100, y_pos)], fill='black', width=2)
    y_pos += 30
    
    # Draw table items
    for description, qty, price in items:
        amount = qty * price
        
        draw.text((col1, y_pos), description, font=normal_font, fill='black')
        draw.text((col2, y_pos), str(qty), font=normal_font, fill='black')
        draw.text((col3, y_pos), f"${price:.2f}", font=normal_font, fill='black')
        draw.text((col4, y_pos), f"${amount:.2f}", font=normal_font, fill='black')
        
        y_pos += 60
    
    # Draw totals
    y_pos = 1500
    draw.line([(col3 - 100, y_pos), (width - 100, y_pos)], fill='black', width=2)
    y_pos += 50
    
    draw.text((col3 - 100, y_pos), "Subtotal:", font=title_font, fill='black')
    draw.text((col4, y_pos), f"${subtotal:.2f}", font=title_font, fill='black')
    y_pos += 60
    
    draw.text((col3 - 100, y_pos), f"Tax ({tax_rate*100:.0f}%):", font=title_font, fill='black')
    draw.text((col4, y_pos), f"${tax_amount:.2f}", font=title_font, fill='black')
    y_pos += 60
    
    draw.line([(col3 - 100, y_pos), (width - 100, y_pos)], fill='black', width=2)
    y_pos += 50
    
    draw.text((col3 - 100, y_pos), "Total:", font=header_font, fill='black')
    draw.text((col4, y_pos), f"${total_amount:.2f}", font=header_font, fill='black')
    
    # Draw payment terms
    y_pos = 2000
    draw.text((100, y_pos), "Payment Terms:", font=title_font, fill='black')
    y_pos += 60
    draw.text((100, y_pos), "Net 30 days. Please make checks payable to " + vendor_name, font=normal_font, fill='black')
    
    # Save the image
    image.save(output_path)
    print(f"Sample invoice created at: {output_path}")

if __name__ == "__main__":
    os.makedirs('sample_invoices', exist_ok=True)
    
    # Generate a few sample invoices
    for i in range(3):
        filename = f"sample_invoices/invoice_{i+1}.png"
        generate_sample_invoice(filename)