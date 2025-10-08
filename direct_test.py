#!/usr/bin/env python3
"""
Direct test of SVG to PDF conversion function
"""
from main import svg_to_pdf
import sys
import os

# Add the current directory to path so we can import main
sys.path.insert(0, os.path.dirname(__file__))


# Simple SVG content
svg_content = """<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
  <rect width="100%" height="100%" fill="lightblue" stroke="navy" stroke-width="2"/>
  <circle cx="150" cy="100" r="50" fill="red" stroke="darkred" stroke-width="3"/>
  <text x="150" y="100" text-anchor="middle" dy=".3em" font-family="Arial" font-size="16" fill="white">Hello PDF!</text>
</svg>"""


def test_svg_conversion():
    print("🔍 Testing SVG to PDF conversion function directly...")

    try:
        # Convert SVG to PDF
        pdf_bytes = svg_to_pdf(svg_content.encode('utf-8'))

        # Check if we got PDF content
        if pdf_bytes and pdf_bytes.startswith(b'%PDF'):
            print(f"✅ Success! Generated PDF with {len(pdf_bytes)} bytes")

            # Save the PDF file
            with open("direct_test_output.pdf", "wb") as f:
                f.write(pdf_bytes)

            print("📄 PDF saved as 'direct_test_output.pdf'")
            return True
        else:
            print("❌ Failed: Generated content is not a valid PDF")
            return False

    except Exception as e:
        print(f"❌ Error during conversion: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Direct SVG to PDF Test\n")
    success = test_svg_conversion()

    if success:
        print("\n🎉 SVG to PDF conversion is working!")
    else:
        print("\n⚠️ SVG to PDF conversion failed")
