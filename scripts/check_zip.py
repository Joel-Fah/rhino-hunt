import binascii
import zipfile

def try_zip():
    zip_file = "contraband.zip" # Ensure this matches your filename
    password = "monkey"
    
    try:
        with zipfile.ZipFile(zip_file) as zf:
            zf.extractall(pwd=password.encode())
            print(f"Success! The password '{password}' works on the actual ZIP file.")
    except Exception as e:
        print(f"Failure: {e}")

if __name__ == "__main__":
    try_zip()
