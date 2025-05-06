# How to Use the Invoice Data Extractor

## Getting Started

1. Make sure you have installed all the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Launch the application:
   ```
   streamlit run app.py
   ```

3. Access the application in your web browser at the provided URL.

## Using the Application

### 1. Upload Invoices

- Click the "Browse files" button to select invoice files.
- You can upload multiple files at once.
- Supported file formats: PDF, JPG, JPEG, PNG.

### 2. Automatic Data Extraction

- After uploading, the system will automatically process each invoice.
- A progress bar will show the status of the extraction process.
- Once complete, the extracted data will be displayed in a table.

### 3. Review and Edit Data

- Check the extracted data for accuracy.
- If any information is missing or incorrect, enable the "Manual Editing" option:
  1. Check the "Enable Manual Editing" checkbox.
  2. Select the invoice row you want to edit from the dropdown.
  3. Edit the fields as needed.
  4. Click "Update Invoice Data" to save your changes.

### 4. Export to Excel

- Enter a filename for your Excel export (or use the default).
- Click the "Export to Excel" button.
- Once the file is created, click "Download Excel File" to save it to your computer.

### 5. Clear Data

- To start fresh, click the "Clear All Data" button in the sidebar.

## Tips for Best Results

1. **Improve Image Quality**:
   - Use high-resolution scans (300 DPI or higher).
   - Ensure the invoice is well-lit and clearly visible.
   - Avoid shadows and glare on the document.

2. **PDF Recommendations**:
   - Use text-based PDFs rather than scanned images when possible.
   - If scanning, use OCR in your scanner software before uploading.

3. **Manual Verification**:
   - Always verify the extracted data, especially for critical fields like invoice numbers and amounts.
   - The application provides an easy way to correct any errors.

4. **Process Similar Invoices Together**:
   - The system works best when processing batches of similar invoice formats.

## Troubleshooting

- **No Text Extracted**: The OCR system may struggle with poor image quality, unusual fonts, or complex layouts. Try improving the scan quality or manually entering the data.

- **Incorrect Data**: If the system repeatedly misidentifies specific fields in your invoices, you may need to adjust the extraction patterns in the code to better match your invoice format.

- **Application Crashes**: If the application crashes during processing, try uploading fewer files at once or files with smaller sizes.

## Sample Invoices

The application includes sample invoices in the `sample_invoices` directory for testing purposes. These samples demonstrate the types of invoices the system can process effectively.