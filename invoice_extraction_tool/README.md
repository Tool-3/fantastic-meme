# Invoice Data Extractor

A Streamlit-based application that extracts key details from invoice PDFs and images, then exports them to Excel.

## Features

- Upload and process multiple invoice files (PDF, JPG, PNG)
- Extract invoice details using OCR and text analysis:
  - Invoice number
  - Invoice date
  - Due date
  - Vendor name
  - Total amount
  - Tax amount
  - Currency
  - Invoice line items
- Manual editing capability for any extracted data
- Export to Excel with one click
- Modern, easy-to-use interface

## Requirements

- Python 3.6+
- Streamlit
- Pandas
- Tesseract OCR
- PyTesseract
- PDF2Image
- PDFPlumber
- OpenCV
- Pillow
- openpyxl

## Deployment on Streamlit Cloud

This application is designed to be deployed directly on Streamlit Cloud free tier:

1. Fork or clone this repository to your GitHub account
2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app from your repository
4. Set the main file path to `app.py`
5. Deploy the app

The `packages.txt` file includes the necessary system dependencies for Streamlit Cloud, and `requirements.txt` lists all Python package requirements.

## Local Installation and Usage

### Install Dependencies

1. Install system dependencies:
   ```
   sudo apt-get install tesseract-ocr libtesseract-dev
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

### Run the App

```
streamlit run app.py
```

## How It Works

1. **Text Extraction**: The app uses PDFPlumber for PDFs and Tesseract OCR for images to extract text content

2. **Data Extraction**: Regular expressions match common invoice patterns to identify key information

3. **Data Management**: Extracted information is stored in a Pandas DataFrame and can be manually edited

4. **Export**: The final data is exported to an Excel file using Pandas

## Limitations

- OCR accuracy depends on the quality of the input files
- Extraction patterns are based on common invoice formats and may not work for all invoice styles
- Complex tables and nested data may not be extracted accurately

## Future Improvements

- Implement machine learning for better text recognition
- Add support for more invoice formats and languages
- Improve line item extraction accuracy
- Implement batch processing for large volumes
- Add database storage for invoice history