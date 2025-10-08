
"""
Tests for pdfvector-ai FastAPI service
"""
from main import app
from fastapi.testclient import TestClient
import os
from io import BytesIO

import pytest

# Set a test API key BEFORE importing the app
TEST_API_KEY = "test-api-key-123"
os.environ["API_KEY"] = TEST_API_KEY


client = TestClient(app)

# Sample SVG content for testing
SAMPLE_SVG = """<?xml version="1.0" encoding="UTF-8"?>
<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>"""


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_convert_svg_json():
    """Test SVG to PDF conversion via JSON endpoint"""
    payload = {
        "svg": SAMPLE_SVG,
        "filename": "circle.pdf"
    }
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.post("/v1/convert/svg", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    assert "circle.pdf" in response.headers["Content-Disposition"]
    assert response.content.startswith(b"%PDF")


def test_convert_svg_file():
    """Test SVG to PDF conversion via file upload endpoint"""
    svg_bytes = SAMPLE_SVG.encode("utf-8")
    files = {"file": ("test.svg", BytesIO(svg_bytes), "image/svg+xml")}
    headers = {"X-API-Key": TEST_API_KEY}
    response = client.post("/v1/convert/svg/file",
                           files=files, headers=headers)
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "test.pdf" in response.headers["Content-Disposition"]
    assert response.content.startswith(b"%PDF")


def test_convert_svg_invalid_api_key():
    """Test conversion with invalid API key"""
    payload = {"svg": SAMPLE_SVG, "filename": "fail.pdf"}
    headers = {"X-API-Key": "wrong-key"}
    response = client.post("/v1/convert/svg", json=payload, headers=headers)
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid API key"


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


== == == =
assert data["service"] == "pdfvector-ai"


def test_health_endpoint_no_auth():
    """Test that health endpoint doesn't require authentication"""
    response = client.get("/health")
    assert response.status_code == 200


def test_convert_svg_json_success():
    """Test successful SVG to PDF conversion via JSON"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": SAMPLE_SVG, "filename": "test.pdf"},
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert "test.pdf" in response.headers["content-disposition"]
    assert len(response.content) > 0
    # Check that it's a PDF file (starts with %PDF)
    assert response.content.startswith(b"%PDF")


def test_convert_svg_json_without_filename():
    """Test SVG to PDF conversion without providing filename"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": SAMPLE_SVG},
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "output.pdf" in response.headers["content-disposition"]


def test_convert_svg_json_filename_without_extension():
    """Test that .pdf extension is added if missing"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": SAMPLE_SVG, "filename": "myfile"},
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 200
    assert "myfile.pdf" in response.headers["content-disposition"]


def test_convert_svg_json_missing_api_key():
    """Test that missing API key returns 401"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": SAMPLE_SVG}
    )
    assert response.status_code == 422  # Missing required header


def test_convert_svg_json_invalid_api_key():
    """Test that invalid API key returns 401"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": SAMPLE_SVG},
        headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]


def test_convert_svg_json_invalid_svg():
    """Test that invalid SVG content returns error"""
    response = client.post(
        "/v1/convert/svg",
        json={"svg": "not valid svg"},
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 400
    assert "Error converting SVG to PDF" in response.json()["detail"]


def test_convert_svg_file_success():
    """Test successful SVG to PDF conversion via file upload"""
    files = {"file": ("test.svg", SAMPLE_SVG.encode(), "image/svg+xml")}
    response = client.post(
        "/v1/convert/svg/file",
        files=files,
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert "test.pdf" in response.headers["content-disposition"]
    assert len(response.content) > 0
    # Check that it's a PDF file
    assert response.content.startswith(b"%PDF")


def test_convert_svg_file_without_extension():
    """Test file upload without .svg extension"""
    files = {"file": ("myfile", SAMPLE_SVG.encode(), "image/svg+xml")}
    response = client.post(
        "/v1/convert/svg/file",
        files=files,
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 200
    assert "myfile.pdf" in response.headers["content-disposition"]


def test_convert_svg_file_missing_api_key():
    """Test that file upload without API key returns error"""
    files = {"file": ("test.svg", SAMPLE_SVG.encode(), "image/svg+xml")}
    response = client.post(
        "/v1/convert/svg/file",
        files=files
    )
    assert response.status_code == 422  # Missing required header


def test_convert_svg_file_invalid_api_key():
    """Test that file upload with invalid API key returns 401"""
    files = {"file": ("test.svg", SAMPLE_SVG.encode(), "image/svg+xml")}
    response = client.post(
        "/v1/convert/svg/file",
        files=files,
        headers={"X-API-Key": "wrong-key"}
    )
    assert response.status_code == 401
    assert "Invalid API key" in response.json()["detail"]


def test_convert_svg_file_invalid_content():
    """Test that invalid file content returns error"""
    files = {"file": ("test.svg", b"not valid svg", "image/svg+xml")}
    response = client.post(
        "/v1/convert/svg/file",
        files=files,
        headers={"X-API-Key": TEST_API_KEY}
    )
    assert response.status_code == 400
    assert "Error converting SVG to PDF" in response.json()["detail"]


>>>>>> > main
