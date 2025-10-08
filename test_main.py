"""
Tests for the FastAPI SVG to PDF conversion service.
"""
import pytest
from fastapi.testclient import TestClient
from main import app
import io

client = TestClient(app)


def test_root_endpoint():
    """Test the root health check endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "message" in data
    assert "version" in data


def test_health_endpoint():
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_convert_valid_svg():
    """Test conversion of a valid SVG file."""
    # Create a simple valid SVG
    svg_content = b'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="blue"/>
</svg>'''
    
    files = {"file": ("test.svg", io.BytesIO(svg_content), "image/svg+xml")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    assert "test.pdf" in response.headers["Content-Disposition"]
    # Check that we got PDF content (PDF files start with %PDF)
    assert response.content.startswith(b"%PDF")


def test_convert_svg_with_vector_graphics():
    """Test conversion of SVG with complex vector graphics."""
    svg_content = b'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
    <rect x="10" y="10" width="80" height="80" fill="red"/>
    <circle cx="150" cy="50" r="40" fill="green"/>
    <path d="M 50 150 L 100 180 L 150 150 Z" fill="yellow"/>
    <text x="50" y="120" font-size="20" fill="black">Vector</text>
</svg>'''
    
    files = {"file": ("vector.svg", io.BytesIO(svg_content), "image/svg+xml")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_convert_without_file():
    """Test conversion endpoint without providing a file."""
    response = client.post("/convert")
    assert response.status_code == 422  # Unprocessable Entity


def test_convert_empty_file():
    """Test conversion of an empty file."""
    files = {"file": ("empty.svg", io.BytesIO(b""), "image/svg+xml")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_convert_invalid_svg():
    """Test conversion of invalid SVG content."""
    invalid_svg = b"This is not valid SVG content"
    
    files = {"file": ("invalid.svg", io.BytesIO(invalid_svg), "image/svg+xml")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 400
    assert "invalid" in response.json()["detail"].lower()


def test_convert_wrong_file_type():
    """Test conversion with non-SVG file."""
    files = {"file": ("test.txt", io.BytesIO(b"plain text"), "text/plain")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 400
    assert "invalid file type" in response.json()["detail"].lower()


def test_convert_svg_without_xml_declaration():
    """Test conversion of SVG without XML declaration."""
    svg_content = b'''<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <rect x="10" y="10" width="80" height="80" fill="purple"/>
</svg>'''
    
    files = {"file": ("simple.svg", io.BytesIO(svg_content), "image/svg+xml")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")


def test_convert_svg_with_filename_extension_check():
    """Test that filename extension is checked when content-type is missing."""
    svg_content = b'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
    <circle cx="50" cy="50" r="40" fill="orange"/>
</svg>'''
    
    # Test with .svg extension but no content-type
    files = {"file": ("test.svg", io.BytesIO(svg_content), "")}
    response = client.post("/convert", files=files)
    
    assert response.status_code == 200
    assert response.content.startswith(b"%PDF")


def test_api_documentation():
    """Test that API documentation is available."""
    response = client.get("/docs")
    assert response.status_code == 200
    
    response = client.get("/openapi.json")
    assert response.status_code == 200
    openapi_spec = response.json()
    assert openapi_spec["info"]["title"] == "PDFVector AI"
