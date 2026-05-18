"""
Code review endpoints for DevAssist API
"""
import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

try:
    from google import genai
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False
    genai = None

from models import (
    ReviewRequest, ReviewResponse, ReviewListItem,
    AddCommentRequest, Comment, SuccessResponse, AIAnalysis
)
from auth import verify_api_key
import mock_data


# Get Gemini API key from environment
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


router = APIRouter(
    prefix="/api/review",
    tags=["Code Review"]
)


def analyze_code_with_gemini(code: str, language: str) -> dict:
    """
    Analyze code using Google Gemini AI
    
    Args:
        code: Code to analyze
        language: Programming language
        
    Returns:
        Dictionary with analysis results
    """
    try:
        if not GENAI_AVAILABLE:
            raise ValueError("google-generativeai package not installed")
        
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not configured")
        
        # Create the client
        client = genai.Client(api_key=GEMINI_API_KEY)  # type: ignore
        
        # Create the prompt
        prompt = f"""You are an expert code reviewer. Analyze the following {language} code and provide a detailed review.

Code:
```{language}
{code}
```

Please provide your analysis in the following JSON format (respond ONLY with valid JSON, no markdown formatting):
{{
    "quality_score": <number between 0-100>,
    "issues": [
        {{
            "severity": "<Critical|Warning|Info>",
            "message": "<issue description>",
            "line": <line number or 0 if general>,
            "suggestion": "<how to fix>"
        }}
    ],
    "suggestions": [
        "<improvement suggestion 1>",
        "<improvement suggestion 2>"
    ],
    "summary": "<overall summary of code quality>",
    "powered_by": "IBM Bob + Gemini AI"
}}

Focus on:
- Code quality and best practices
- Potential bugs or security issues
- Performance optimizations
- Readability and maintainability
- Design patterns and architecture
"""
        
        # Generate response
        response = client.models.generate_content(model='gemini-1.5-flash', contents=prompt)  # type: ignore
        
        # Parse the response
        response_text = response.text.strip()  # type: ignore
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        
        # Parse JSON
        analysis = json.loads(response_text)
        
        # Ensure powered_by is set
        analysis["powered_by"] = "IBM Bob + Gemini AI"
        
        return analysis
        
    except json.JSONDecodeError as e:
        # Fallback if JSON parsing fails
        return {
            "quality_score": 75,
            "issues": [
                {
                    "severity": "Info",
                    "message": "AI analysis completed but response format was unexpected",
                    "line": 0,
                    "suggestion": "Manual review recommended"
                }
            ],
            "suggestions": [
                "Consider adding more comments",
                "Review error handling"
            ],
            "summary": "Code analysis completed with AI assistance. Some formatting issues in AI response.",
            "powered_by": "IBM Bob + Gemini AI"
        }
    except Exception as e:
        # Fallback for any other errors
        return {
            "quality_score": 70,
            "issues": [
                {
                    "severity": "Warning",
                    "message": f"AI analysis error: {str(e)}",
                    "line": 0,
                    "suggestion": "Check API configuration and try again"
                }
            ],
            "suggestions": [
                "Verify GEMINI_API_KEY is set correctly",
                "Check network connectivity"
            ],
            "summary": "Unable to complete full AI analysis. Using fallback analysis.",
            "powered_by": "IBM Bob + Gemini AI"
        }


@router.post(
    "/submit",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit code for review",
    description="Submit a code snippet for AI-powered review and get detailed analysis"
)
async def submit_review(
    review_request: ReviewRequest,
    api_key: str = Depends(verify_api_key)
) -> ReviewResponse:
    """
    Submit code for AI-powered review using Google Gemini.
    
    Args:
        review_request: Code review request with code, language, and metadata
        
    Returns:
        Created review with AI analysis including quality score, issues, and suggestions
    """
    try:
        # Analyze code with Gemini AI
        ai_analysis = analyze_code_with_gemini(
            review_request.code,
            review_request.language
        )
        
        # Create review with AI analysis
        review = mock_data.create_mock_review(
            title=review_request.title,
            code=review_request.code,
            language=review_request.language,
            description=review_request.description
        )
        
        # Convert dict to AIAnalysis model
        review.ai_analysis = AIAnalysis(**ai_analysis)
        
        return review
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create review: {str(e)}"
        )


@router.get(
    "/{review_id}",
    response_model=ReviewResponse,
    summary="Get review details",
    description="Retrieve detailed information about a specific review"
)
async def get_review(
    review_id: str,
    api_key: str = Depends(verify_api_key)
) -> ReviewResponse:
    """
    Get review by ID.
    
    Args:
        review_id: Unique review identifier
        
    Returns:
        Review details including code, comments, and status
        
    Raises:
        HTTPException: If review not found
    """
    review = mock_data.get_review_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID '{review_id}' not found"
        )
    
    return review


@router.get(
    "/list",
    response_model=List[ReviewListItem],
    summary="List all reviews",
    description="Get a list of all code reviews with summary information"
)
async def list_reviews(api_key: str = Depends(verify_api_key)) -> List[ReviewListItem]:
    """
    List all reviews.
    
    Returns:
        List of review summaries
    """
    reviews = mock_data.get_all_reviews()
    
    # Convert to list items
    review_items = [
        ReviewListItem(
            review_id=review.review_id,
            title=review.title,
            status=review.status,
            language=review.language,
            comment_count=len(review.comments),
            created_at=review.created_at
        )
        for review in reviews
    ]
    
    return review_items


@router.put(
    "/{review_id}/comment",
    response_model=Comment,
    summary="Add comment to review",
    description="Add a new comment to an existing code review"
)
async def add_comment(
    review_id: str,
    comment_request: AddCommentRequest,
    api_key: str = Depends(verify_api_key)
) -> Comment:
    """
    Add a comment to a review.
    
    Args:
        review_id: Review identifier
        comment_request: Comment details including line number and message
        
    Returns:
        Created comment
        
    Raises:
        HTTPException: If review not found
    """
    # Check if review exists
    review = mock_data.get_review_by_id(review_id)
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID '{review_id}' not found"
        )
    
    # Add comment
    comment = mock_data.add_comment_to_review(
        review_id=review_id,
        line_number=comment_request.line_number,
        message=comment_request.message,
        severity=comment_request.severity
    )
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add comment"
        )
    
    return comment


@router.delete(
    "/{review_id}",
    response_model=SuccessResponse,
    summary="Delete review",
    description="Delete a code review by ID"
)
async def delete_review(
    review_id: str,
    api_key: str = Depends(verify_api_key)
) -> SuccessResponse:
    """
    Delete a review (mock implementation).
    
    Args:
        review_id: Review identifier
        
    Returns:
        Success response
        
    Raises:
        HTTPException: If review not found
    """
    review = mock_data.get_review_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID '{review_id}' not found"
        )
    
    # In a real implementation, this would delete from database
    # For mock, we'll just return success
    return SuccessResponse(
        success=True,
        message=f"Review '{review_id}' deleted successfully",
        data={"review_id": review_id}
    )


@router.get(
    "/{review_id}/comments",
    response_model=List[Comment],
    summary="Get review comments",
    description="Get all comments for a specific review"
)
async def get_review_comments(
    review_id: str,
    api_key: str = Depends(verify_api_key)
) -> List[Comment]:
    """
    Get all comments for a review.
    
    Args:
        review_id: Review identifier
        
    Returns:
        List of comments
        
    Raises:
        HTTPException: If review not found
    """
    review = mock_data.get_review_by_id(review_id)
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Review with ID '{review_id}' not found"
        )
    
    return review.comments

# Made with Bob
