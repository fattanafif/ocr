"""make_sample.py — Generate sample.png to test the new OCR solver."""
import cv2
import numpy as np

img = np.ones((60, 180, 3), dtype=np.uint8) * 255
cv2.putText(img, "8K9P2", (20, 42), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (10, 10, 10), 2)
cv2.imwrite("sample.png", img)
print("Generated sample.png with text 8K9P2")
