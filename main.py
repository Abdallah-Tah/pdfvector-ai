"""
FastAPI service for vector-safe SVG to PDF conversion.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import Response
import cairosvg
from xml.etree.ElementTree import ParseError
from urllib.error import URLError
import io

app = FastAPI(
    title="PDFVector AI",
    description="Vector-safe PDF conversion API (SVG → PDF)",
    version="1.0.0"
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "PDFVector AI - SVG to PDF Conversion API",
        "status": "online",
        "version": "1.0.0"
    }


@app.post("/convert", response_class=Response)
async def convert_svg_to_pdf(file: UploadFile = File(...)):
    """
    Convert SVG file to PDF format.
    
    Args:
        file: SVG file to convert (multipart/form-data)
        
    Returns:
        PDF file as bytes with application/pdf content type
        
    Raises:
        HTTPException: If file is not valid SVG or conversion fails
    """
    # Validate file type
    if not file.content_type or "svg" not in file.content_type.lower():
        # Also check filename extension
        if not file.filename or not file.filename.lower().endswith(".svg"):
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Please upload an SVG file."
            )
    
    try:
        # Read SVG content
        svg_content = await file.read()
        
        # Validate that it's valid SVG content
        if not svg_content:
            raise HTTPException(
                status_code=400,
                detail="Empty file provided"
            )
        
        # Convert SVG to PDF using CairoSVG
        # CairoSVG preserves vector graphics, ensuring quality
        pdf_bytes = cairosvg.svg2pdf(bytestring=svg_content)
        
        # Return PDF with appropriate headers
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={file.filename.rsplit('.', 1)[0]}.pdf"
            }
        )
        
    except ParseError as e:
        # Handle SVG parsing errors
        raise HTTPException(
            status_code=400,
            detail=f"Invalid SVG file: {str(e)}"
        )
    except URLError as e:
        # Handle empty or invalid file errors
        raise HTTPException(
            status_code=400,
            detail="Invalid or empty SVG file"
        )
    except HTTPException:
        # Re-raise HTTPExceptions as-is
        raise
    except Exception as e:
        # Handle other conversion errors
        error_message = str(e)
        raise HTTPException(
            status_code=500,
            detail=f"Conversion failed: {error_message}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {"status": "healthy"}
