#!/usr/bin/env python3
import os
import requests
import tempfile

BASE_URL = os.getenv("PDFVECTOR_BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("API_KEY", "dev-key")  # must match server .env

SVG = """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="lightblue" stroke="navy" stroke-width="2"/>
  <circle cx="150" cy="100" r="50" fill="red" stroke="darkred" stroke-width="3"/>
  <text x="150" y="100" text-anchor="middle" dy=".3em" font-family="Arial" font-size="16" fill="white">Hello PDF!</text>
</svg>""".strip()

S = requests.Session()
S.headers.update({"X-API-Key": API_KEY})


def must_ok(r):
    r.raise_for_status()
    return r


def health():
    r = must_ok(S.get(f"{BASE_URL}/health", timeout=10))
    print("health:", r.json())


def json_convert():
    r = must_ok(S.post(f"{BASE_URL}/v1/convert/svg",
                       json={"svg": SVG, "filename": "test_output.pdf"},
                       timeout=30))
    assert r.content.startswith(b"%PDF")
    with open("test_output.pdf", "wb") as f:
        f.write(r.content)
    print("json → PDF ok:", len(r.content), "bytes")


def file_convert():
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False) as tmp:
        tmp.write(SVG)
        tmp.flush()
        with open(tmp.name, "rb") as f:
            r = must_ok(S.post(f"{BASE_URL}/v1/convert/svg/file",
                               files={
                                   "file": ("test.svg", f, "image/svg+xml")},
                               timeout=30))
    assert r.content.startswith(b"%PDF")
    with open("test_output_file.pdf", "wb") as f:
        f.write(r.content)
    print("file → PDF ok:", len(r.content), "bytes")


if __name__ == "__main__":
    print("BASE_URL:", BASE_URL)
    health()
    json_convert()
    file_convert()
    print("✅ All tests passed.")
