from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

import sys

try:
    img = Image.open('test.jpg')
    img.save('extracted_gator_REPAIRED.jpg')
    print("Success")
except Exception as e:
    print(f"Error: {e}")
