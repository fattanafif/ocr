#!/usr/bin/env python3
"""solve.py

Universal Command-line tool to solve any captcha image using the ONNX OCR Engine.

Supports:
1. Local Image File paths (e.g. `python solve.py sample.png`)
2. Base64 Image strings (e.g. `python solve.py "iVBORw0KGgoAAAANSUhEUgAA..."`)

Usage:
    python solve.py <file_path_or_base64_string>
"""

import sys
import os
import time
from ocr_engine import OCREngine

def main():
    if len(sys.argv) < 2:
        print("Usage: python solve.py <file_path_or_base64_string>")
        sys.exit(1)

    input_data = sys.argv[1].strip()

    t0 = time.perf_counter()
    engine = OCREngine()
    try:
        result = engine.predict_auto(input_data)
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

        if os.path.isfile(input_data):
            print(f"Input Type    : File ({input_data})")
        else:
            print(f"Input Type    : Base64 String ({len(input_data)} chars)")

        print(f"Author        : @Real_zezomod")
        print(f"Solve Time    : {elapsed_ms} ms")
        print(f"Result        : {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
