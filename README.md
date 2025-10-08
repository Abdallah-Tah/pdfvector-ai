# pdfvector-ai
Vector-safe PDF conversion API (SVG → PDF) built with FastAPI.

## Features

- 🚀 Fast and efficient SVG to PDF conversion
- 🎨 Vector-safe conversion preserving graphics quality
- 📝 RESTful API built with FastAPI
- ✅ Comprehensive test suite
- 📚 Auto-generated API documentation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Abdallah-Tah/pdfvector-ai.git
cd pdfvector-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the API server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Health Check
```bash
GET /
GET /health
```

#### Convert SVG to PDF
```bash
POST /convert
Content-Type: multipart/form-data
```

**Example:**
```bash
curl -F "file=@example.svg" http://localhost:8000/convert -o output.pdf
```

### API Documentation

Interactive API documentation is automatically generated and available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest test_main.py -v
```

## Example SVG

Create a test SVG file:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
    <rect x="10" y="10" width="80" height="80" fill="red"/>
    <circle cx="150" cy="50" r="40" fill="green"/>
    <text x="50" y="120" font-size="20" fill="black">Vector Graphics</text>
</svg>
```

Convert it to PDF:
```bash
curl -F "file=@test.svg" http://localhost:8000/convert -o output.pdf
```

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **CairoSVG**: SVG to PDF conversion library that preserves vector graphics
- **Uvicorn**: ASGI server for running the application
- **Pytest**: Testing framework

## License

MIT
