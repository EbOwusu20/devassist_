# DevAssist - Code Review & Analysis API

A powerful FastAPI backend for code review and analysis, providing comprehensive tools for developers to improve code quality.

## Features

- 🔍 **Code Analysis** - Analyze code quality, complexity, and metrics
- 📝 **Code Review** - Submit and manage code reviews with comments
- 📚 **Documentation** - Access coding guidelines and best practices
- 🔐 **API Key Authentication** - Simple and secure token-based authentication
- 🚀 **Fast & Async** - Built with FastAPI for high performance
- 📖 **Auto-generated Docs** - Interactive API documentation with Swagger UI

## Project Structure

```
DevAssist/
├── main.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── auth.py                # API key authentication
├── models.py              # Pydantic data models
├── mock_data.py           # Mock data for development
├── routes/
│   ├── __init__.py       # Routes package
│   ├── analyse.py        # Code analysis endpoints
│   ├── review.py         # Code review endpoints
│   └── docs.py           # Documentation endpoints
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── ARCHITECTURE.md       # Detailed architecture documentation
└── README.md             # This file
```

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd DevAssist
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your preferred settings
   # Update API_KEYS with your own secure keys
   ```

### Running the Application

**Development mode (with auto-reload):**
```bash
python main.py
```

**Or using uvicorn directly:**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Production mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

The API will be available at:
- **API Base URL:** http://localhost:8000
- **Interactive Docs (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## API Authentication

All API endpoints (except root, health, and info) require authentication using an API key.

**Include the API key in the request header:**
```
X-API-Key: your-api-key-here
```

**Example using curl:**
```bash
curl -X GET "http://localhost:8000/api/docs/guidelines" \
  -H "X-API-Key: dev-key-123"
```

**Example using Python requests:**
```python
import requests

headers = {"X-API-Key": "dev-key-123"}
response = requests.get("http://localhost:8000/api/docs/guidelines", headers=headers)
print(response.json())
```

## API Endpoints

### Root & Health

- `GET /` - API information
- `GET /health` - Health check
- `GET /api/info` - Detailed API information

### Code Analysis (`/api/analyse`)

- `POST /api/analyse/code` - Analyze code snippet
- `GET /api/analyse/metrics` - Get code metrics examples
- `POST /api/analyse/complexity` - Calculate complexity score
- `POST /api/analyse/validate` - Validate code syntax

### Code Review (`/api/review`)

- `POST /api/review/submit` - Submit code for review
- `GET /api/review/{review_id}` - Get review details
- `GET /api/review/list` - List all reviews
- `PUT /api/review/{review_id}/comment` - Add comment to review
- `DELETE /api/review/{review_id}` - Delete review
- `GET /api/review/{review_id}/comments` - Get review comments

### Documentation (`/api/docs`)

- `GET /api/docs/guidelines` - Get coding guidelines
- `GET /api/docs/best-practices` - Get best practices
- `POST /api/docs/search` - Search documentation
- `GET /api/docs/categories` - Get documentation categories
- `GET /api/docs/languages` - Get supported languages
- `GET /api/docs/guidelines/{language}` - Get language-specific guidelines
- `GET /api/docs/best-practices/{practice_id}` - Get best practice by ID

## Usage Examples

### Analyze Code

```bash
curl -X POST "http://localhost:8000/api/analyse/code" \
  -H "X-API-Key: dev-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello():\n    print(\"Hello, World!\")",
    "language": "python",
    "filename": "hello.py"
  }'
```

### Submit Code Review

```bash
curl -X POST "http://localhost:8000/api/review/submit" \
  -H "X-API-Key: dev-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "function add(a, b) { return a + b; }",
    "language": "javascript",
    "title": "Add Function Review",
    "description": "Please review this simple add function"
  }'
```

### Get Coding Guidelines

```bash
curl -X GET "http://localhost:8000/api/docs/guidelines?language=python" \
  -H "X-API-Key: dev-key-123"
```

### Search Documentation

```bash
curl -X POST "http://localhost:8000/api/docs/search" \
  -H "X-API-Key: dev-key-123" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "error handling",
    "language": "python"
  }'
```

## Supported Programming Languages

- Python
- JavaScript
- TypeScript
- Java
- C#
- Go
- Rust
- C++
- PHP
- Ruby

## Configuration

Edit the `.env` file to customize:

```env
# Application Settings
APP_NAME=DevAssist
DEBUG=true
HOST=0.0.0.0
PORT=8000

# API Keys (comma-separated)
API_KEYS=dev-key-123,test-key-456,prod-key-789

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
```

## Development

### Project Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed architecture documentation, including:
- Component details
- Data flow diagrams
- Error handling patterns
- API design patterns

### Adding New Endpoints

1. Create or modify route files in the `routes/` directory
2. Define Pydantic models in `models.py`
3. Add mock data functions in `mock_data.py` (if needed)
4. Register the router in `main.py`

### Testing

Access the interactive API documentation at http://localhost:8000/docs to test all endpoints directly in your browser.

## Error Handling

The API returns standardized error responses:

**401 Unauthorized:**
```json
{
  "error": "Authentication failed",
  "message": "Invalid or missing API key",
  "type": "AuthenticationError"
}
```

**404 Not Found:**
```json
{
  "error": "Resource not found",
  "message": "Review with ID 'xyz' not found",
  "type": "ResourceNotFoundError"
}
```

**422 Validation Error:**
```json
{
  "detail": [
    {
      "loc": ["body", "code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Production Deployment

### Security Recommendations

1. **Generate secure API keys:**
   ```python
   import secrets
   api_key = secrets.token_urlsafe(32)
   ```

2. **Use environment variables** for sensitive configuration
3. **Enable HTTPS** in production
4. **Set DEBUG=false** in production
5. **Configure proper CORS origins**
6. **Use a production ASGI server** (uvicorn with workers)

### Docker Deployment (Optional)

Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t devassist .
docker run -p 8000:8000 --env-file .env devassist
```

## Contributing

1. Follow PEP 8 style guidelines
2. Add type hints to all functions
3. Document new endpoints in this README
4. Update ARCHITECTURE.md for significant changes
5. Test all endpoints before committing

## License

This project is provided as-is for educational and development purposes.

## Support

For issues, questions, or contributions, please refer to the project documentation or contact the development team.

---

**Built with ❤️ using FastAPI**