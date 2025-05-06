# Setup Instructions for Invoice Data Extractor on Streamlit Cloud

## Quick Deployment Guide

Follow these steps to deploy this application on Streamlit Cloud's free tier:

### Step 1: Fork the Repository

1. Go to the GitHub repository containing this code
2. Click the "Fork" button in the top-right corner
3. Wait for GitHub to create your fork of the repository

### Step 2: Deploy on Streamlit Cloud

1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your forked repository
5. In the "Main file path" field, enter: `app.py`
6. Click "Deploy"

That's it! Streamlit Cloud will automatically recognize the `packages.txt` file and install the required system dependencies, and the `requirements.txt` file for Python packages.

## Testing Locally (Optional)

If you want to test the application locally before deploying:

1. Clone your forked repository:
   ```
   git clone https://github.com/YOUR-USERNAME/invoice-extractor.git
   cd invoice-extractor
   ```

2. Install system dependencies:
   ```
   sudo apt-get install tesseract-ocr libtesseract-dev
   ```

3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Troubleshooting Deployment Issues

If you encounter issues with the deployment on Streamlit Cloud:

1. **Check Logs**: In the Streamlit Cloud dashboard, click on your app and check the logs for any error messages.

2. **Package Versions**: If there are package conflicts, try adjusting the versions in `requirements.txt` to be compatible with Streamlit Cloud.

3. **Memory Limits**: Remember that Streamlit Cloud's free tier has memory limitations. If your app crashes, it might be processing files that are too large.

4. **GitHub Actions**: The included GitHub Actions workflow (`test.yml`) will automatically test the app's dependencies whenever you push to the main branch, which can help identify issues before deployment.

## Notes for Streamlit Cloud Deployment

- The free tier has resource limitations: max 1GB RAM and up to 1 hour of inactivity before sleeping
- The app can process multiple invoices, but very large batches might exceed memory limits
- File upload is limited to 50MB per file by default (configured in `.streamlit/config.toml`)
- No database persistence between sessions (data is stored in session state only)