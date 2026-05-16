# DevAssist - Google Gemini AI Integration Setup

## Overview
DevAssist has been upgraded with Google Gemini AI integration for real-time code analysis and documentation generation. This guide will help you set up and run the system.

## What's New

### 1. **AI-Powered Code Review** (`routes/review.py`)
- Uses Google Gemini `gemini-2.0-flash` model
- Provides intelligent code analysis with:
  - Quality score (0-100)
  - Detailed issue detection with severity levels
  - Line-specific suggestions
  - Overall code summary
  - Powered by: IBM Bob + Gemini AI

### 2. **AI-Powered Documentation Generation** (`routes/docs.py`)
- Uses Google Gemini `gemini-2.0-flash` model
- Generates comprehensive documentation including:
  - Docstrings in proper format
  - README sections
  - Plain English explanations
  - Parameter and return documentation
  - Usage examples
  - Powered by: IBM Bob + Gemini AI

### 3. **Enhanced Frontend** (`script.js`)
- Displays AI analysis results beautifully
- Shows quality scores prominently
- Lists issues with severity indicators
- Presents improvement suggestions
- Real-time API integration

## Prerequisites

1. **Python 3.8+** installed
2. **Google Gemini API Key** - Get yours at: https://makersuite.google.com/app/apikey

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- Uvicorn (ASGI server)
- Pydantic (data validation)
- python-dotenv (environment variables)
- google-generativeai (Gemini AI SDK)

### 2. Configure Environment Variables

The `.env` file has been created from `.env.example`. Update it with your actual Gemini API key:

```bash
# Open .env file and replace the placeholder
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

**Important:** Keep your API key secure and never commit it to version control!

### 3. Start the Backend Server

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### 4. Open the Frontend

Open `index.html` in your web browser. You can:
- Double-click the file, or
- Use a local server (recommended):

```bash
# Python 3
python -m http.server 8080

# Then open: http://localhost:8080
```

## Usage Guide

### Code Review with AI

1. Navigate to the **Code Review** tab
2. Enter your code in the text area
3. Select the programming language
4. Click **Submit Review**
5. View AI-powered analysis including:
   - Quality score out of 100
   - List of issues with severity levels
   - Improvement suggestions
   - Overall summary

### Documentation Generation with AI

1. First, enter code in the **Code Review** tab
2. Navigate to the **Documentation** tab
3. Select documentation type (README, API, etc.)
4. Click **Generate Documentation**
5. View AI-generated documentation including:
   - Docstrings
   - README sections
   - Plain English explanations
   - Parameter documentation
   - Usage examples

### Repository Analysis

1. Navigate to the **Repository Analysis** tab
2. Enter repository URL
3. Select analysis options
4. Click **Analyze Repository**
5. View comprehensive analysis results

## API Endpoints

### Code Review
- **POST** `/api/review/submit` - Submit code for AI review
- **GET** `/api/review/{review_id}` - Get review details
- **GET** `/api/review/list` - List all reviews

### Documentation
- **POST** `/api/docs/generate` - Generate AI documentation
- **GET** `/api/docs/guidelines` - Get coding guidelines
- **GET** `/api/docs/best-practices` - Get best practices

### Health Check
- **GET** `/health` - Check API health
- **GET** `/` - API information

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Configuration

### Environment Variables (.env)

```bash
# Application Settings
APP_NAME=DevAssist
DEBUG=true
HOST=0.0.0.0
PORT=8000

# API Keys (comma-separated)
API_KEYS=dev-key-123,test-key-456,prod-key-789

# CORS Origins (comma-separated)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,http://127.0.0.1:3000

# Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here
```

### Frontend Configuration (script.js)

Update the API endpoint and key in `script.js` if needed:

```javascript
const response = await fetch('http://localhost:8000/api/review/submit', {
    headers: {
        'X-API-Key': 'dev-key-123' // Use your actual API key
    }
});
```

## Error Handling

The system includes comprehensive error handling:

1. **Missing API Key**: Falls back to basic analysis with warning
2. **API Errors**: Provides fallback responses with error details
3. **Network Issues**: Shows user-friendly error messages
4. **Invalid Input**: Validates all inputs before processing

## Features

### AI-Powered Analysis
- ✅ Real-time code quality scoring
- ✅ Intelligent issue detection
- ✅ Context-aware suggestions
- ✅ Multi-language support
- ✅ Security and performance analysis

### Documentation Generation
- ✅ Automatic docstring generation
- ✅ README section creation
- ✅ Plain English explanations
- ✅ Parameter documentation
- ✅ Usage examples

### User Experience
- ✅ Clean, modern interface
- ✅ Real-time feedback
- ✅ Loading indicators
- ✅ Smooth animations
- ✅ Responsive design

## Troubleshooting

### Issue: "GEMINI_API_KEY not configured"
**Solution:** Ensure your `.env` file has the correct API key set.

### Issue: API returns 401 Unauthorized
**Solution:** Check that your X-API-Key header matches one of the keys in API_KEYS.

### Issue: CORS errors in browser
**Solution:** Add your frontend URL to CORS_ORIGINS in `.env`.

### Issue: Module 'google.generativeai' not found
**Solution:** Run `pip install google-generativeai`.

### Issue: Frontend can't connect to backend
**Solution:** Ensure the backend is running on port 8000 and update the URL in script.js if needed.

## Security Notes

1. **Never commit `.env` file** - It's in `.gitignore`
2. **Use strong API keys** in production
3. **Rotate API keys** regularly
4. **Limit CORS origins** to trusted domains
5. **Use HTTPS** in production

## Development

### Project Structure
```
DevAssist/
├── main.py                 # Application entry point (loads .env)
├── config.py              # Configuration management
├── models.py              # Pydantic models (includes AIAnalysis)
├── auth.py                # API key authentication
├── mock_data.py           # Mock data for testing
├── routes/
│   ├── review.py          # AI-powered code review
│   ├── docs.py            # AI-powered documentation
│   └── analyse.py         # Repository analysis
├── index.html             # Frontend interface
├── script.js              # Frontend logic (AI results display)
├── styles.css             # Styling
├── .env                   # Environment variables (not in git)
├── .env.example           # Environment template
└── requirements.txt       # Python dependencies
```

### Key Changes Made

1. **main.py**: Added `python-dotenv` to load environment variables before imports
2. **models.py**: Added `AIAnalysis` model for structured AI responses
3. **routes/review.py**: Integrated Gemini AI for code analysis
4. **routes/docs.py**: Integrated Gemini AI for documentation generation
5. **script.js**: Updated to display AI results with quality scores, issues, and suggestions
6. **.env.example**: Added GEMINI_API_KEY placeholder
7. **requirements.txt**: Added google-generativeai dependency

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation at `/docs`
3. Check console logs for detailed error messages

## Powered By

**IBM Bob + Gemini AI** - Combining expert software engineering with cutting-edge AI technology.

---

Made with ❤️ by Bob