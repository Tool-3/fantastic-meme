# Troubleshooting Tesseract OCR Issues

If you're encountering issues with Tesseract OCR in the Invoice Data Extractor application, this guide will help you resolve them.

## Common Error Messages

### "tesseract is not installed or it's not in your PATH"

This error occurs when the application cannot find the Tesseract OCR executable on your system. Here's how to fix it:

## Installation Instructions

### Windows

1. Download the installer from [UB-Mannheim's GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. **Important**: During installation, check the box that says "Add to PATH"
4. Restart your computer after installation
5. Verify by opening Command Prompt and typing: `tesseract --version`

### macOS

Using Homebrew:
```
brew install tesseract
```

Verify installation:
```
tesseract --version
```

### Linux

Ubuntu/Debian:
```
sudo apt-get update
sudo apt-get install tesseract-ocr libtesseract-dev
```

Fedora/RHEL/CentOS:
```
sudo dnf install tesseract tesseract-devel
```

Verify installation:
```
tesseract --version
```

## Manual Configuration in Python

If Tesseract is installed but Python can't find it, you need to set the path manually:

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Windows example
```

## Streamlit Cloud Configuration

For Streamlit Cloud deployment:

1. Ensure your `packages.txt` file includes:
   ```
   tesseract-ocr
   libtesseract-dev
   ```

2. After updating packages.txt, redeploy your application

## Verifying Installation

To verify Tesseract is working correctly with Python:

```python
import pytesseract
print(pytesseract.get_tesseract_version())
```

If this returns a version number, Tesseract is correctly configured.

## Running the Tesseract Helper

This application includes a Tesseract helper utility that can diagnose issues:

```
streamlit run tesseract_helper.py
```

This utility will:
- Check if Tesseract is installed and configured correctly
- Attempt to locate Tesseract on your system
- Provide detailed installation instructions
- Show your current configuration

## What If Tesseract Still Doesn't Work?

If you continue having issues with Tesseract:

1. PDF extraction will still work without Tesseract
2. Use the manual editing feature to fill in data that couldn't be extracted
3. Consider using online OCR services for your images before uploading them

## Additional Resources

- [Tesseract OCR Documentation](https://github.com/tesseract-ocr/tesseract)
- [PyTesseract Documentation](https://github.com/madmaze/pytesseract)
- [Tesseract OCR Installation Guide](https://tesseract-ocr.github.io/tessdoc/Installation.html)