import os
import cv2
import numpy as np

BASE_DIR = "storage"

def save_file(path: str, content: bytes) -> str:
    """
    Save uploaded file content as .jpg regardless of original format.
    """
    # Decode to OpenCV image
    arr = np.frombuffer(content, np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Invalid image file")

    # Force .jpg extension
    if not path.lower().endswith(".jpg"):
        path = os.path.splitext(path)[0] + ".jpg"

    # Ensure directories exist
    abs_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)

    # Save as JPEG
    cv2.imwrite(abs_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), 95])

    return abs_path
