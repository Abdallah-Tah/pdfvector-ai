# pdfvector-ai

Vector-safe PDF conversion API (SVG → PDF) built with FastAPI.

## Features

- Convert SVG to vector PDF with preserved quality
- Two conversion endpoints: JSON payload and file upload
- API key authentication for secure access
- Health check endpoint for monitoring
- Docker support for easy deployment
- Comprehensive test suite

## Requirements

- Python 3.11+
- Cairo graphics library (for SVG rendering)

## Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/Abdallah-Tah/pdfvector-ai.git
cd pdfvector-ai
```

2. Install system dependencies (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 libffi-dev shared-mime-info
```

3. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and set your API_KEY
```

6. Run the application:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t pdfvector-ai .
```

2. Run the container:
```bash
docker run -d -p 8000:8000 -e API_KEY=your-secret-key pdfvector-ai
```

## API Endpoints

### Health Check

**GET** `/health`

Check if the service is running.

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "pdfvector-ai"
}
```

### Convert SVG (JSON)

**POST** `/v1/convert/svg`

Convert SVG content from JSON payload to PDF.

**Headers:**
- `X-API-Key`: Your API key (required)
- `Content-Type`: application/json

**Body:**
```json
{
  "svg": "<svg>...</svg>",
  "filename": "output.pdf"  // optional
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/v1/convert/svg \
  -H "X-API-Key: your-secret-key" \
  -H "Content-Type: application/json" \
  -d '{
    "svg": "<?xml version=\"1.0\" encoding=\"UTF-8\"?><svg width=\"100\" height=\"100\" xmlns=\"http://www.w3.org/2000/svg\"><circle cx=\"50\" cy=\"50\" r=\"40\" fill=\"red\"/></svg>",
    "filename": "circle.pdf"
  }' \
  --output circle.pdf
```

### Convert SVG (File Upload)

**POST** `/v1/convert/svg/file`

Convert uploaded SVG file to PDF.

**Headers:**
- `X-API-Key`: Your API key (required)

**Form Data:**
- `file`: SVG file to upload

**Example:**
```bash
curl -X POST http://localhost:8000/v1/convert/svg/file \
  -H "X-API-Key: your-secret-key" \
  -F "file=@path/to/your/image.svg" \
  --output converted.pdf
```

## Authentication

All conversion endpoints require authentication via the `X-API-Key` header. Set your API key in the `.env` file:

```bash
API_KEY=your-secret-api-key-here
```

## Testing

Run the test suite:

```bash
pytest -v test_main.py
```

Run tests with coverage:

```bash
pytest --cov=main --cov-report=html test_main.py
```

## Deployment

### Heroku

1. Create a new Heroku app:
```bash
heroku create your-app-name
```

2. Set the API key:
```bash
heroku config:set API_KEY=your-secret-key
```

3. Deploy:
```bash
git push heroku main
```

### Docker

The included Dockerfile can be used to deploy on any container platform (AWS ECS, Google Cloud Run, Azure Container Instances, etc.).

## Environment Variables

- `API_KEY` (required): Secret key for API authentication
- `PORT` (optional): Port to run the service on (default: 8000)

## License

MIT

## Contributing

Pull requests are welcome! Please ensure tests pass before submitting.

## API Documentation

Once the service is running, you can access:
- Interactive API docs (Swagger UI): http://localhost:8000/docs
- Alternative API docs (ReDoc): http://localhost:8000/redoc
