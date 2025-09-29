import os
from PIL import Image
import pytesseract
import io

TESS_CMD = os.getenv("TESSERACT_CMD")
if TESS_CMD:
    pytesseract.pytesseract.tesseract_cmd = TESS_CMD

def run_ocr(image_bytes: bytes):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        text = pytesseract.image_to_string(img)
        # confidence is engine-specific; for now we return None
        return text.strip(), None
    except Exception as e:
        return "", None
