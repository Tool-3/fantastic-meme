import streamlit as st
import os
import platform
import subprocess
import sys
import pytesseract

def check_tesseract_installation():
    """Check if Tesseract OCR is installed and available"""
    try:
        # Try to get the tesseract version
        version = pytesseract.get_tesseract_version()
        st.success(f"✅ Tesseract OCR v{version} is installed and working correctly")
        return True
    except Exception as e:
        st.error(f"❌ Tesseract OCR is not installed or not properly configured: {e}")
        
        # Provide platform-specific installation instructions
        system = platform.system()
        if system == 'Windows':
            st.info("""
            ## Windows Installation Instructions
            
            1. Download the installer from [UB-Mannheim's GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
            2. Run the installer (check "Add to PATH" during installation)
            3. Restart your command prompt/IDE after installation
            4. Verify by running `tesseract --version` in command prompt
            """)
        elif system == 'Darwin':  # macOS
            st.info("""
            ## macOS Installation Instructions
            
            Using Homebrew:
            ```
            brew install tesseract
            ```
            
            Verify installation:
            ```
            tesseract --version
            ```
            """)
        elif system == 'Linux':
            st.info("""
            ## Linux Installation Instructions
            
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
            """)
        
        st.info("""
        ## For Streamlit Cloud Deployment
        
        1. Ensure your `packages.txt` file includes:
           ```
           tesseract-ocr
           libtesseract-dev
           ```
        
        2. Redeploy your application
        """)
        
        return False

def locate_tesseract_binary():
    """Try to find the Tesseract binary path"""
    system = platform.system()
    paths = []
    
    if system == 'Windows':
        paths = [
            r'C:\Program Files\Tesseract-OCR\tesseract.exe',
            r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
        ]
    elif system == 'Darwin':  # macOS
        paths = [
            '/usr/local/bin/tesseract',
            '/opt/homebrew/bin/tesseract'
        ]
    else:  # Linux and others
        paths = [
            '/usr/bin/tesseract',
            '/usr/local/bin/tesseract'
        ]
    
    # Try to find tesseract in PATH first
    try:
        output = subprocess.check_output(['which', 'tesseract'], stderr=subprocess.STDOUT, text=True)
        if output:
            path = output.strip()
            st.info(f"Found Tesseract at: {path}")
            return path
    except:
        pass
    
    # Check known paths
    for path in paths:
        if os.path.exists(path):
            st.info(f"Found Tesseract at: {path}")
            return path
    
    st.warning("Could not find Tesseract binary in common locations")
    return None

def main():
    st.title("Tesseract OCR Troubleshooter")
    
    st.write("This tool helps verify your Tesseract OCR installation and configuration.")
    
    if check_tesseract_installation():
        st.success("Your Tesseract installation is working correctly!")
        
        # Show configuration details
        st.subheader("Configuration Details")
        tesseract_path = pytesseract.pytesseract.tesseract_cmd
        st.code(f"Tesseract Path: {tesseract_path}")
        
        # Get available languages
        try:
            languages = pytesseract.get_languages()
            st.write("Installed languages:")
            st.code(", ".join(languages))
        except:
            st.warning("Could not retrieve installed languages")
    else:
        # Try to locate tesseract binary
        binary_path = locate_tesseract_binary()
        
        if binary_path:
            st.info("Trying to configure pytesseract with the found path...")
            try:
                pytesseract.pytesseract.tesseract_cmd = binary_path
                version = pytesseract.get_tesseract_version()
                st.success(f"Successfully configured! Tesseract v{version} is now accessible.")
            except Exception as e:
                st.error(f"Configuration failed: {e}")
                
    st.write("---")
    st.write("After installing Tesseract, restart your application to use the OCR capabilities.")
    
if __name__ == "__main__":
    main()