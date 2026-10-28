# CaptchaX OCR Solver API & CLI

High-speed, offline OCR Captcha recognition server and CLI tool powered by ONNX Runtime and ddddocr neural network models.

**Author**: `@Real_zezomod`

---

## Key Features

- **Fast Inference**: Sub-millisecond CTC decoding powered by ONNX C++ runtime engine.
- **Universal Inputs**: Accepts local image files, raw Base64 strings, or Data URIs (`data:image/png;base64,...`).
- **REST API Server**: Built-in HTTP server with automatic port recovery and JSON endpoints.
- **Cross-Platform**: Full support for Windows, Linux, and macOS.

---

## Requirements & Installation

### Requirements
- Python 3.10+
- Dependencies: `opencv-python`, `onnxruntime`, `numpy`

### Installation
```bash
pip install opencv-python onnxruntime numpy
```

---

## Quick Start

### 1. Command Line Solver (`solve.py`)

Solve a local image file:
```bash
python solve.py sample.png
```

Solve a Base64 string directly:
```bash
python solve.py "iVBORw0KGgoAAAANSUhEUgAA..."
```

**Output**:
```text
Input Type    : File (sample.png)
Author        : @Real_zezomod
Solve Time    : 14.25 ms
Result        : 8K9P2
```

---

### 2. HTTP REST API Server (`server.py`)

Start the API server (default port `5000`):
```bash
python server.py 5000
```

#### Endpoint Specification

`POST /solve`

**Headers**: `Content-Type: application/json`

**Request Body**:
```json
{
  "image": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

**Response**:
```json
{
  "status": "success",
  "result": "8K9P2",
  "Author": "@Real_zezomod",
  "solve_time_ms": "14.25 ms"
}
```

---

## Integration Examples

### Python
```python
import requests
import base64

with open("sample.png", "rb") as f:
    b64_data = base64.b64encode(f.read()).decode()

response = requests.post("http://localhost:5000/solve", json={"image": b64_data})
print(response.json())
```

### cURL
```bash
curl -X POST http://localhost:5000/solve \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$(base64 -w 0 sample.png)\"}"
```

### Node.js
```javascript
const fs = require('fs');

const b64 = fs.readFileSync('sample.png', 'base64');

fetch('http://localhost:5000/solve', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ image: b64 })
})
  .then(res => res.json())
  .then(console.log);
```
