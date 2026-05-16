"""
Code analysis endpoints for DevAssist API
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict
from models import (
    CodeSnippet, AnalysisResult, CodeMetrics, 
    ProgrammingLanguage, SuccessResponse
)
from auth import verify_api_key
import mock_data


router = APIRouter(
    prefix="/api/analyse",
    tags=["Code Analysis"],
    dependencies=[Depends(verify_api_key)]
)


@router.post(
    "/code",
    response_model=AnalysisResult,
    summary="Analyze code snippet",
    description="Analyze a code snippet and return complexity, issues, and metrics"
)
async def analyze_code(code_snippet: CodeSnippet) -> AnalysisResult:
    """
    Analyze a code snippet for quality, complexity, and potential issues.
    
    Args:
        code_snippet: Code to analyze with language specification
        
    Returns:
        Analysis results including complexity score, issues, and metrics
    """
    try:
        result = mock_data.get_mock_analysis_result(
            code_snippet.code,
            code_snippet.language
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )


@router.get(
    "/metrics",
    response_model=Dict[str, CodeMetrics],
    summary="Get code metrics examples",
    description="Get example code metrics for different complexity levels"
)
async def get_metrics_examples() -> Dict[str, CodeMetrics]:
    """
    Get example code metrics for reference.
    
    Returns:
        Dictionary of example metrics for different code quality levels
    """
    return {
        "excellent": CodeMetrics(
            lines_of_code=50,
            cyclomatic_complexity=3,
            maintainability_index=95.0,
            comment_ratio=0.25
        ),
        "good": CodeMetrics(
            lines_of_code=100,
            cyclomatic_complexity=8,
            maintainability_index=75.0,
            comment_ratio=0.15
        ),
        "needs_improvement": CodeMetrics(
            lines_of_code=200,
            cyclomatic_complexity=15,
            maintainability_index=50.0,
            comment_ratio=0.05
        ),
        "poor": CodeMetrics(
            lines_of_code=500,
            cyclomatic_complexity=25,
            maintainability_index=25.0,
            comment_ratio=0.02
        )
    }


@router.post(
    "/complexity",
    response_model=Dict[str, int],
    summary="Calculate complexity score",
    description="Calculate cyclomatic complexity for a code snippet"
)
async def calculate_complexity(code_snippet: CodeSnippet) -> Dict[str, int]:
    """
    Calculate the cyclomatic complexity of a code snippet.
    
    Args:
        code_snippet: Code to analyze
        
    Returns:
        Dictionary with complexity score and line count
    """
    try:
        lines = code_snippet.code.split('\n')
        loc = len([line for line in lines if line.strip()])
        
        # Simple mock complexity calculation
        # In a real implementation, this would use proper AST analysis
        complexity = min(100, loc * 2)
        cyclomatic = min(20, loc // 5 + 1)
        
        return {
            "complexity_score": complexity,
            "cyclomatic_complexity": cyclomatic,
            "lines_of_code": loc
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Complexity calculation failed: {str(e)}"
        )


@router.post(
    "/validate",
    response_model=SuccessResponse,
    summary="Validate code syntax",
    description="Check if code has valid syntax for the specified language"
)
async def validate_syntax(code_snippet: CodeSnippet) -> SuccessResponse:
    """
    Validate code syntax (mock implementation).
    
    Args:
        code_snippet: Code to validate
        
    Returns:
        Success response with validation result
    """
    # Mock validation - always returns success
    # In a real implementation, this would use language-specific parsers
    return SuccessResponse(
        success=True,
        message=f"Code syntax is valid for {code_snippet.language.value}",
        data={
            "language": code_snippet.language.value,
            "lines": len(code_snippet.code.split('\n'))
        }
    )

# Made with Bob
