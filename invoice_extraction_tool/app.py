import streamlit as st
import pandas as pd
import os
import tempfile
import cv2
import numpy as np
import pytesseract
from PIL import Image
import pdfplumber
import re
from datetime import datetime
import uuid
import io

# Set page configuration
st.set_page_config(
    page_title="Invoice Data Extractor",
    page_icon="📊",
    layout="wide"
)

# App title and description
st.title("Invoice Data Extractor")
st.markdown("Upload PDF or image invoices to extract data and export to Excel")

# Define columns for the fields we want to extract
invoice_columns = [
    "Invoice Number", 
    "Invoice Date", 
    "Due Date", 
    "Vendor Name", 
    "Total Amount", 
    "Tax Amount",
    "Currency",
    "Invoice Items",
    "Source File"
]

# Initialize the dataframe to store extracted data if it doesn't exist in session state
if 'extracted_data' not in st.session_state:
    st.session_state.extracted_data = pd.DataFrame(columns=invoice_columns)

# Function to extract text from PDF files
def extract_text_from_pdf(file):
    text = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
    return text

# Function to extract text from image files
def extract_text_from_image(file):
    try:
        # Read the image
        image = Image.open(file)
        # Convert to OpenCV format
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Preprocessing for better OCR results
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        
        # Extract text using pytesseract
        text = pytesseract.image_to_string(thresh)
        return text
    except Exception as e:
        st.error(f"Error extracting text from image: {e}")
        return ""

# Function to extract invoice details using regex patterns
def extract_invoice_details(text, filename):
    details = {}
    
    # Initialize default values
    for col in invoice_columns:
        details[col] = ""
    
    # Set the source filename
    details["Source File"] = filename
    
    # Extract invoice number (various formats)
    invoice_num_patterns = [
        r'(?i)Invoice\s*(?:#|No|Number|Num)[:.\s]*([A-Z0-9\-_]+)',
        r'(?i)Invoice\s*ID[:.\s]*([A-Z0-9\-_]+)',
        r'(?i)Invoice[:.\s]*([A-Z0-9\-_]+)',
    ]
    
    for pattern in invoice_num_patterns:
        match = re.search(pattern, text)
        if match:
            details["Invoice Number"] = match.group(1).strip()
            break
    
    # Extract invoice date
    date_patterns = [
        r'(?i)Invoice\s*Date[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        r'(?i)Date[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        r'(?i)Date\s*Issued[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        r'(?i)Issued\s*Date[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            details["Invoice Date"] = match.group(1).strip()
            break
    
    # Extract due date
    due_date_patterns = [
        r'(?i)Due\s*Date[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
        r'(?i)Payment\s*Due[:.\s]*(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})',
    ]
    
    for pattern in due_date_patterns:
        match = re.search(pattern, text)
        if match:
            details["Due Date"] = match.group(1).strip()
            break
    
    # Extract vendor name
    vendor_patterns = [
        r'(?i)Vendor\s*Name[:.\s]*([A-Za-z0-9\s\.,&\-\']+)(?=\n)',
        r'(?i)Supplier[:.\s]*([A-Za-z0-9\s\.,&\-\']+)(?=\n)',
        r'(?i)From[:.\s]*([A-Za-z0-9\s\.,&\-\']+)(?=\n)',
        r'(?i)Seller[:.\s]*([A-Za-z0-9\s\.,&\-\']+)(?=\n)',
    ]
    
    for pattern in vendor_patterns:
        match = re.search(pattern, text)
        if match:
            details["Vendor Name"] = match.group(1).strip()
            break
    
    # If no vendor name found, try to find it from the top of the invoice
    if not details["Vendor Name"]:
        lines = text.split('\n')
        for i in range(min(5, len(lines))):  # Check first 5 lines
            if lines[i] and not any(keyword in lines[i].lower() for keyword in ['invoice', 'bill', 'receipt', 'statement']):
                details["Vendor Name"] = lines[i].strip()
                break
    
    # Extract total amount
    total_patterns = [
        r'(?i)Total(?:\s*Amount)?[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)Amount\s*Due[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)Grand\s*Total[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)Balance\s*Due[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
    ]
    
    for pattern in total_patterns:
        match = re.search(pattern, text)
        if match:
            details["Total Amount"] = match.group(1).strip()
            break
    
    # Extract tax amount
    tax_patterns = [
        r'(?i)Tax(?:\s*Amount)?[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)VAT[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)GST[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
        r'(?i)Sales\s*Tax[:.\s]*[\$\€\£]?\s*([\d,]+\.\d{2})',
    ]
    
    for pattern in tax_patterns:
        match = re.search(pattern, text)
        if match:
            details["Tax Amount"] = match.group(1).strip()
            break
    
    # Extract currency
    currency_patterns = [
        r'(?i)Currency[:.\s]*([A-Z]{3})',
        r'[\$\€\£\¥]',  # Currency symbols
    ]
    
    for pattern in currency_patterns:
        match = re.search(pattern, text)
        if match:
            if match.group(0) == '$':
                details["Currency"] = 'USD'
            elif match.group(0) == '€':
                details["Currency"] = 'EUR'
            elif match.group(0) == '£':
                details["Currency"] = 'GBP'
            elif match.group(0) == '¥':
                details["Currency"] = 'JPY'
            else:
                details["Currency"] = match.group(1).strip()
            break
    
    # Try to extract items
    # Look for patterns that might indicate item tables in invoices
    items_text = ""
    items_patterns = [
        r'(?i)Item\s*Description(.*?)(?:Total|Balance|Due)',
        r'(?i)Description\s*Quantity\s*Rate(.*?)(?:Total|Balance|Due)',
        r'(?i)Product\s*Description(.*?)(?:Total|Balance|Due)',
    ]
    
    for pattern in items_patterns:
        match = re.search(pattern, text, re.DOTALL)
        if match:
            items_text = match.group(1).strip()
            break
    
    # Simplify items text - just grab a few lines
    if items_text:
        items_lines = items_text.split('\n')
        items_text = '\n'.join(items_lines[:min(5, len(items_lines))])
        
    details["Invoice Items"] = items_text
    
    return details

# Main functionality
def main():
    # Sidebar for actions
    st.sidebar.header("Actions")
    
    # File uploader
    uploaded_files = st.file_uploader("Upload Invoice Files (PDF or Image)", 
                                      type=["pdf", "jpg", "jpeg", "png"], 
                                      accept_multiple_files=True)
    
    # If files are uploaded
    if uploaded_files:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Process each uploaded file
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Process file directly from memory instead of writing to disk
            if uploaded_file.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                extracted_text = extract_text_from_image(uploaded_file)
            elif uploaded_file.name.lower().endswith('.pdf'):
                extracted_text = extract_text_from_pdf(uploaded_file)
            else:
                st.warning(f"Unsupported file type: {uploaded_file.name}")
                continue
            
            # Extract invoice details
            invoice_details = extract_invoice_details(extracted_text, uploaded_file.name)
            
            # Add to session state dataframe
            st.session_state.extracted_data = pd.concat([
                st.session_state.extracted_data,
                pd.DataFrame([invoice_details])
            ], ignore_index=True)
            
            # Update progress
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text("Processing complete!")
        progress_bar.empty()
    
    # Display extracted data
    if not st.session_state.extracted_data.empty:
        st.subheader("Extracted Invoice Data")
        st.dataframe(st.session_state.extracted_data)
        
        # Manual editing functionality
        if st.checkbox("Enable Manual Editing"):
            st.info("Select a row to edit its details")
            
            # Select row to edit
            row_indices = st.session_state.extracted_data.index.tolist()
            selected_row = st.selectbox("Select invoice to edit", row_indices)
            
            if selected_row is not None:
                with st.form("edit_form"):
                    st.subheader(f"Edit Invoice: {st.session_state.extracted_data.loc[selected_row, 'Source File']}")
                    
                    edited_data = {}
                    for col in invoice_columns:
                        if col != "Source File" and col != "Invoice Items":
                            edited_data[col] = st.text_input(col, st.session_state.extracted_data.loc[selected_row, col])
                    
                    edited_data["Invoice Items"] = st.text_area("Invoice Items", st.session_state.extracted_data.loc[selected_row, "Invoice Items"])
                    
                    # Submit button
                    if st.form_submit_button("Update Invoice Data"):
                        for col in edited_data:
                            st.session_state.extracted_data.loc[selected_row, col] = edited_data[col]
                        st.success("Invoice data updated!")
        
        # Export to Excel
        export_filename = st.text_input("Excel filename", f"invoice_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx")
        
        if st.button("Export to Excel"):
            if not export_filename.endswith('.xlsx'):
                export_filename += '.xlsx'
                
            # Create Excel in memory
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                st.session_state.extracted_data.to_excel(writer, index=False)
            
            # Provide download link
            st.download_button(
                label="Download Excel File",
                data=buffer,
                file_name=export_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success(f"Data exported to {export_filename} successfully!")
        
        # Clear data button
        if st.sidebar.button("Clear All Data"):
            st.session_state.extracted_data = pd.DataFrame(columns=invoice_columns)
            st.experimental_rerun()

# Run the main function
if __name__ == "__main__":
    main()