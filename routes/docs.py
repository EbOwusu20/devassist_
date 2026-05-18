"""
Documentation endpoints for DevAssist API
"""
import os
import json
import logging
from fastapi import APIRouter, Depends, Query, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel, Field
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from models import (
    GuidelineResponse, BestPractice, SearchRequest,
    SearchResult, ProgrammingLanguage
)
from auth import verify_api_key
import mock_data


# Get Groq API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if GROQ_API_KEY:
    logger.info("GROQ_API_KEY found in environment")
else:
    logger.warning("GROQ_API_KEY not found in environment")


router = APIRouter(
    prefix="/api/docs",
    tags=["Documentation"]
)


def generate_docstring_with_gemini(code: str, language: str) -> dict:
    """
    Generate documentation using Groq AI
    
    Args:
        code: Code to document
        language: Programming language
        
    Returns:
        Dictionary with documentation
    """
    try:
        logger.info(f"Starting documentation generation for {language} code")
        
        if not GROQ_API_KEY:
            error_msg = "GROQ_API_KEY not configured in environment variables"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Initialize Groq client
        client = Groq(api_key=os.getenv('GROQ_API_KEY'))
        
        # Create the prompt
        prompt = f"""You are an expert technical writer. Generate comprehensive documentation for the following {language} code.

Code:
```{language}
{code}
```

Please provide your documentation in the following JSON format (respond ONLY with valid JSON, no markdown formatting):
{{
    "docstring": "<detailed docstring/documentation comment for the code>",
    "readme_section": "<README.md section describing this code>",
    "plain_english": "<plain English explanation of what the code does>",
    "parameters": [
        {{
            "name": "<parameter name>",
            "type": "<parameter type>",
            "description": "<what this parameter does>"
        }}
    ],
    "returns": "<description of what the code returns>",
    "examples": [
        "<usage example 1>",
        "<usage example 2>"
    ],
    "powered_by": "IBM Bob + Groq AI"
}}

Focus on:
- Clear, concise explanations
- Proper formatting for the language
- Practical usage examples
- Complete parameter and return documentation
"""
        
        # Make API call to Groq
        logger.info("Sending request to Groq API")
        response = client.chat.completions.create(
            model='llama3-8b-8192',
            messages=[{'role': 'user', 'content': prompt}],
            max_tokens=1000
        )
        
        # Extract text from response
        response_text = response.choices[0].message.content
        if response_text:
            response_text = response_text.strip()
        else:
            response_text = ""
        
        logger.debug(f"Raw response: {response_text[:200]}...")
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        logger.info("Parsing JSON response")
        documentation = json.loads(response_text)
        
        # Ensure powered_by is set
        documentation["powered_by"] = "IBM Bob + Groq AI"
        
        logger.info("Documentation generated successfully")
        return documentation
        
    except json.JSONDecodeError as e:
        error_msg = f"JSON parsing error: {str(e)}"
        logger.error(error_msg)
        logger.error(f"Failed to parse response text: {response_text[:500] if 'response_text' in locals() and response_text else 'N/A'}")
        
        # Fallback if JSON parsing fails
        return {
            "docstring": f"# Documentation for {language} code\n\nAI-generated documentation (format error)",
            "readme_section": f"## Code Documentation\n\nThis section contains {language} code.",
            "plain_english": "This code performs operations as defined in the implementation.",
            "parameters": [],
            "returns": "Result of the operation",
            "examples": ["# See code for usage"],
            "powered_by": "IBM Bob + Groq AI",
            "error": error_msg
        }
    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__}: {str(e)}"
        logger.error(error_msg)
        logger.exception("Full traceback:")
        
        # Fallback for any other errors
        return {
            "docstring": f"# Documentation\n\nError generating documentation: {str(e)}",
            "readme_section": f"## Code Section\n\nDocumentation generation encountered an error.",
            "plain_english": "Unable to generate full documentation. Please check API configuration.",
            "parameters": [],
            "returns": "Unknown",
            "examples": ["# Documentation generation failed"],
            "powered_by": "IBM Bob + Groq AI",
            "error": error_msg
        }


class DocumentationRequest(BaseModel):
    """Request model for documentation generation"""
    code: str = Field(..., description="Code to document")
    language: ProgrammingLanguage = Field(..., description="Programming language")


@router.post(
    "/generate",
    summary="Generate documentation",
    description="Generate AI-powered documentation for code including docstrings, README sections, and plain English descriptions"
)
async def generate_documentation(
    request: DocumentationRequest,
    api_key: str = Depends(verify_api_key)
) -> dict:
    """
    Generate comprehensive documentation for code using Google Gemini AI.
    
    Args:
        request: Documentation request with code and language
        
    Returns:
        Generated documentation including docstrings, README sections, and descriptions
    """
    try:
        logger.info(f"Documentation generation request for language: {request.language.value}")
        logger.debug(f"Code length: {len(request.code)} characters")
        
        documentation = generate_docstring_with_gemini(request.code, request.language.value)
        
        # Check if there was an error in the documentation generation
        if "error" in documentation:
            logger.warning(f"Documentation generated with error: {documentation['error']}")
        
        return documentation
    except ValueError as e:
        # Configuration or validation errors
        error_msg = str(e)
        logger.error(f"Configuration error: {error_msg}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Configuration error: {error_msg}"
        )
    except Exception as e:
        # Unexpected errors
        error_msg = f"{type(e).__name__}: {str(e)}"
        logger.error(f"Unexpected error in generate_documentation: {error_msg}")
        logger.exception("Full traceback:")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate documentation: {error_msg}"
        )


@router.get(
    "/guidelines",
    response_model=GuidelineResponse,
    summary="Get coding guidelines",
    description="Retrieve coding guidelines and best practices for a specific language or general guidelines"
)
async def get_guidelines(
    language: Optional[ProgrammingLanguage] = Query(
        None,
        description="Programming language to get guidelines for"
    ),
    api_key: str = Depends(verify_api_key)
) -> GuidelineResponse:
    """
    Get coding guidelines.
    
    Args:
        language: Optional programming language filter
        
    Returns:
        Coding guidelines with rules and examples
    """
    return mock_data.get_guidelines(language)


@router.get(
    "/best-practices",
    response_model=List[BestPractice],
    summary="Get best practices",
    description="Retrieve coding best practices, optionally filtered by language"
)
async def get_best_practices(
    language: Optional[ProgrammingLanguage] = Query(
        None,
        description="Filter by programming language"
    ),
    category: Optional[str] = Query(
        None,
        description="Filter by category (e.g., Security, Performance)"
    ),
    api_key: str = Depends(verify_api_key)
) -> List[BestPractice]:
    """
    Get best practices.
    
    Args:
        language: Optional language filter
        category: Optional category filter
        
    Returns:
        List of best practices
    """
    practices = mock_data.get_best_practices(language)
    
    # Filter by category if provided
    if category:
        practices = [
            p for p in practices 
            if p.category.lower() == category.lower()
        ]
    
    return practices


@router.post(
    "/search",
    response_model=List[SearchResult],
    summary="Search documentation",
    description="Search through guidelines and best practices"
)
async def search_documentation(
    search_request: SearchRequest,
    api_key: str = Depends(verify_api_key)
) -> List[SearchResult]:
    """
    Search documentation.
    
    Args:
        search_request: Search query with optional filters
        
    Returns:
        List of search results with relevance scores
    """
    results = mock_data.search_documentation(
        query=search_request.query,
        category=search_request.category,
        language=search_request.language
    )
    
    # Convert to SearchResult models
    search_results = [
        SearchResult(
            result_type=result["result_type"],
            title=result["title"],
            description=result["description"],
            relevance_score=result["relevance_score"]
        )
        for result in results
    ]
    
    # Sort by relevance score
    search_results.sort(key=lambda x: x.relevance_score, reverse=True)
    
    return search_results


@router.get(
    "/categories",
    response_model=List[str],
    summary="Get documentation categories",
    description="Get list of available documentation categories"
)
async def get_categories(api_key: str = Depends(verify_api_key)) -> List[str]:
    """
    Get available documentation categories.
    
    Returns:
        List of category names
    """
    # Extract unique categories from best practices
    practices = mock_data.get_best_practices()
    categories = list(set(p.category for p in practices))
    categories.sort()
    
    return categories


@router.get(
    "/languages",
    response_model=List[str],
    summary="Get supported languages",
    description="Get list of supported programming languages"
)
async def get_supported_languages(api_key: str = Depends(verify_api_key)) -> List[str]:
    """
    Get supported programming languages.
    
    Returns:
        List of supported language names
    """
    return [lang.value for lang in ProgrammingLanguage]


@router.get(
    "/guidelines/{language}",
    response_model=GuidelineResponse,
    summary="Get language-specific guidelines",
    description="Get coding guidelines for a specific programming language"
)
async def get_language_guidelines(
    language: ProgrammingLanguage,
    api_key: str = Depends(verify_api_key)
) -> GuidelineResponse:
    """
    Get guidelines for a specific language.
    
    Args:
        language: Programming language
        
    Returns:
        Language-specific coding guidelines
    """
    return mock_data.get_guidelines(language)


@router.get(
    "/best-practices/{practice_id}",
    response_model=BestPractice,
    summary="Get best practice by ID",
    description="Retrieve a specific best practice by its ID"
)
async def get_best_practice_by_id(
    practice_id: str,
    api_key: str = Depends(verify_api_key)
) -> BestPractice:
    """
    Get a specific best practice by ID.
    
    Args:
        practice_id: Best practice identifier
        
    Returns:
        Best practice details
    """
    practices = mock_data.get_best_practices()
    practice = next((p for p in practices if p.practice_id == practice_id), None)
    
    if not practice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Best practice with ID '{practice_id}' not found"
        )
    
    return practice

# Made with Bob
