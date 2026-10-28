#!/usr/bin/env python3
"""server.py

Fast HTTP REST API Server for Captcha Solving powered by ddddocr ONNX model.

Endpoints:
  POST /solve
    Payload: JSON {"image": "base64_string"} or raw Base64 string
    Returns: JSON {
      "status": "success",
      "result": "CAPTCHA_TEXT",
      "Author": "@Real_zezomod",
      "solve_time_ms": "12.34 ms"
    }

  GET /
    Returns: JSON {"status": "running", "engine": "ddddocr ONNX Engine", "Author": "@Real_zezomod"}

Usage:
  python server.py [port]
"""

import os
import sys
import json
import time
import socket
import base64
from http.server import HTTPServer, BaseHTTPRequestHandler
from ocr_engine import OCREngine

ENGINE = OCREngine()

class ReusableHTTPServer(HTTPServer):
    allow_reuse_address = True

class CaptchaHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress standard HTTP access logs for clean console
        pass

    def send_json(self, status_code: int, data: dict):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def do_POST(self):
        if self.path not in ["/solve", "/solve/"]:
            return self.send_json(404, {
                "status": "error",
                "message": "Endpoint not found",
                "Author": "@Real_zezomod"
            })

        t0 = time.perf_counter()
        try:
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")

            b64_str = body
            try:
                data = json.loads(body)
                if isinstance(data, dict) and "image" in data:
                    b64_str = data["image"]
            except Exception:
                pass

            if "," in b64_str:
                b64_str = b64_str.split(",", 1)[1]

            image_bytes = base64.b64decode(b64_str)
            text = ENGINE.predict_bytes(image_bytes)
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

            self.send_json(200, {
                "status": "success",
                "result": text,
                "Author": "@Real_zezomod",
                "solve_time_ms": f"{elapsed_ms} ms"
            })
        except Exception as e:
            elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)
            self.send_json(400, {
                "status": "error",
                "message": str(e),
                "Author": "@Real_zezomod",
                "solve_time_ms": f"{elapsed_ms} ms"
            })

    def do_GET(self):
        self.send_json(200, {
            "status": "running",
            "engine": "ddddocr ONNX Engine",
            "Author": "@Real_zezomod"
        })

def run(preferred_port: int = 5000):
    ports_to_try = [preferred_port, 5001, 8000, 8080, 5050]
    httpd = None
    active_port = None

    for port in ports_to_try:
        try:
            server_address = ("0.0.0.0", port)
            httpd = ReusableHTTPServer(server_address, CaptchaHandler)
            active_port = port
            break
        except (PermissionError, OSError, socket.error):
            continue

    if not httpd:
        print("[ERROR] Could not bind HTTP server to any available port.")
        sys.exit(1)

    print(f"==================================================")
    print(f"  OCR Captcha Solver REST API Server")
    print(f"  Author : @Real_zezomod")
    print(f"  URL    : http://localhost:{active_port}/solve")
    print(f"==================================================")
    httpd.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    run(port)
