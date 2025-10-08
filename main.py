"""
FastAPI service for converting SVG to vector PDF
"""
import os
from io import BytesIO
from typing import Optional
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fastapi import FastAPI, HTTPException, Security, UploadFile, File, Header
from fastapi.responses import Response
from pydantic import BaseModel, Field
import os
from io import BytesIO
from typing import Optional

# import cairosvg
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from fastapi import FastAPI, HTTPException, Security, UploadFile, File, Header
from fastapi.responses import Response
from pydantic import BaseModel, Field


app = FastAPI(
    title="pdfvector-ai",
    description="Vector-safe PDF conversion API (SVG → PDF)",
    version="1.0.0"
)


API_KEY = os.getenv("API_KEY", "")


def svg_to_pdf(svg_content: bytes) -> bytes:
    """
    Convert SVG content to PDF using svglib and reportlab
    Args:
        svg_content: SVG content as bytes
    Returns:
        PDF content as bytes
    """
    try:
        svg_io = BytesIO(svg_content)
        rlg_drawing = svg2rlg(svg_io)
        pdf_buffer = BytesIO()
        renderPDF.drawToFile(rlg_drawing, pdf_buffer)
        pdf_buffer.seek(0)
        return pdf_buffer.getvalue()
    except Exception as e:
        raise Exception(f"SVG to PDF conversion failed: {str(e)}")


class SVGConvertRequest(BaseModel):
    """Request model for SVG conversion"""
    svg: str = Field(..., description="SVG content as string")
    filename: Optional[str] = Field(
        None, description="Optional output filename")


async def verify_api_key(x_api_key: str = Header(..., alias="X-API-Key")):
    """Verify the API key from the request header"""
    if not API_KEY:
        raise HTTPException(
            status_code=500, detail="API_KEY not configured on server")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "pdfvector-ai"}


@app.post("/v1/convert/svg")
async def convert_svg_json(request: SVGConvertRequest, api_key: str = Security(verify_api_key)):
    """
    Convert SVG to PDF from JSON payload
    Args:
        request: SVGConvertRequest with svg content and optional filename
        api_key: API key from X-API-Key header
    Returns:
        PDF file as response with appropriate Content-Disposition header
    """
    try:
        pdf_data = svg_to_pdf(request.svg.encode('utf-8'))
        filename = request.filename if request.filename else "output.pdf"
        if not filename.endswith('.pdf'):
            filename += '.pdf'
        return Response(content=pdf_data, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{filename}"'})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error converting SVG to PDF: {str(e)}")


@app.post("/v1/convert/svg/file")
async def convert_svg_file(file: UploadFile = File(...), api_key: str = Security(verify_api_key)):
    """
    Convert SVG to PDF from uploaded file
    Args:
        file: Uploaded SVG file
        api_key: API key from X-API-Key header
    Returns:
        PDF file as response with appropriate Content-Disposition header
    """
    try:
        svg_content = await file.read()
        pdf_data = svg_to_pdf(svg_content)
        original_filename = file.filename or "output"
        if original_filename.endswith('.svg'):
            pdf_filename = original_filename[:-4] + '.pdf'
        else:
            pdf_filename = original_filename + '.pdf'
        return Response(content=pdf_data, media_type="application/pdf", headers={"Content-Disposition": f'attachment; filename="{pdf_filename}"'})
    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error converting SVG to PDF: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
