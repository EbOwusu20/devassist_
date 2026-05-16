"""
Pydantic models for request/response validation
"""
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field


# Enums
class ProgrammingLanguage(str, Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    CPP = "cpp"
    PHP = "php"
    RUBY = "ruby"


class ReviewStatus(str, Enum):
    """Review status options"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REJECTED = "rejected"


class IssueSeverity(str, Enum):
    """Issue severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


# Code Analysis Models
class CodeSnippet(BaseModel):
    """Input code for analysis"""
    code: str = Field(..., description="The code to analyze", min_length=1)
    language: ProgrammingLanguage = Field(..., description="Programming language")
    filename: Optional[str] = Field(None, description="Optional filename")


class Issue(BaseModel):
    """Code issue found during analysis"""
    line_number: int = Field(..., description="Line number where issue occurs", ge=1)
    message: str = Field(..., description="Issue description")
    severity: IssueSeverity = Field(..., description="Issue severity level")
    rule_id: Optional[str] = Field(None, description="Rule identifier")


class CodeMetrics(BaseModel):
    """Code quality metrics"""
    lines_of_code: int = Field(..., description="Total lines of code", ge=0)
    cyclomatic_complexity: int = Field(..., description="Cyclomatic complexity score", ge=1)
    maintainability_index: float = Field(..., description="Maintainability index (0-100)", ge=0, le=100)
    comment_ratio: float = Field(..., description="Ratio of comments to code", ge=0, le=1)


class AnalysisResult(BaseModel):
    """Analysis output"""
    complexity_score: int = Field(..., description="Overall complexity score", ge=0, le=100)
    issues: List[Issue] = Field(default_factory=list, description="List of found issues")
    metrics: CodeMetrics = Field(..., description="Code metrics")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    analyzed_at: datetime = Field(default_factory=datetime.utcnow, description="Analysis timestamp")


# Code Review Models
class ReviewRequest(BaseModel):
    """Submit code for review"""
    code: str = Field(..., description="Code to review", min_length=1)
    language: ProgrammingLanguage = Field(..., description="Programming language")
    title: str = Field(..., description="Review title", min_length=1, max_length=200)
    description: Optional[str] = Field(None, description="Optional description", max_length=1000)


class Comment(BaseModel):
    """Review comment"""
    comment_id: str = Field(..., description="Unique comment identifier")
    line_number: int = Field(..., description="Code line reference", ge=1)
    message: str = Field(..., description="Comment text", min_length=1)
    severity: IssueSeverity = Field(..., description="Issue severity")
    author: str = Field(default="DevAssist", description="Comment author")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Comment timestamp")


class AIAnalysis(BaseModel):
    """AI-powered code analysis results"""
    quality_score: int = Field(..., description="Code quality score (0-100)", ge=0, le=100)
    issues: List[Dict[str, Any]] = Field(default_factory=list, description="List of issues found")
    suggestions: List[str] = Field(default_factory=list, description="Improvement suggestions")
    summary: str = Field(..., description="Overall analysis summary")
    powered_by: str = Field(default="IBM Bob + Gemini AI", description="AI provider")


class ReviewResponse(BaseModel):
    """Review details"""
    review_id: str = Field(..., description="Unique review identifier")
    title: str = Field(..., description="Review title")
    status: ReviewStatus = Field(..., description="Review status")
    language: ProgrammingLanguage = Field(..., description="Programming language")
    code: str = Field(..., description="Code being reviewed")
    comments: List[Comment] = Field(default_factory=list, description="Review comments")
    description: Optional[str] = Field(None, description="Review description")
    ai_analysis: Optional[AIAnalysis] = Field(None, description="AI-powered analysis results")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")


class ReviewListItem(BaseModel):
    """Simplified review item for list view"""
    review_id: str = Field(..., description="Unique review identifier")
    title: str = Field(..., description="Review title")
    status: ReviewStatus = Field(..., description="Review status")
    language: ProgrammingLanguage = Field(..., description="Programming language")
    comment_count: int = Field(default=0, description="Number of comments", ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")


class AddCommentRequest(BaseModel):
    """Add comment to a review"""
    line_number: int = Field(..., description="Code line reference", ge=1)
    message: str = Field(..., description="Comment text", min_length=1, max_length=500)
    severity: IssueSeverity = Field(default=IssueSeverity.INFO, description="Issue severity")


# Documentation Models
class Rule(BaseModel):
    """Coding rule"""
    rule_id: str = Field(..., description="Rule identifier")
    title: str = Field(..., description="Rule title")
    description: str = Field(..., description="Rule description")
    examples: List[str] = Field(default_factory=list, description="Code examples")


class GuidelineResponse(BaseModel):
    """Coding guidelines"""
    category: str = Field(..., description="Guideline category")
    rules: List[Rule] = Field(..., description="List of rules")
    language: Optional[ProgrammingLanguage] = Field(None, description="Specific language")


class BestPractice(BaseModel):
    """Best practice item"""
    practice_id: str = Field(..., description="Practice identifier")
    title: str = Field(..., description="Practice title")
    description: str = Field(..., description="Practice description")
    category: str = Field(..., description="Category")
    language: Optional[ProgrammingLanguage] = Field(None, description="Specific language")
    code_example: Optional[str] = Field(None, description="Code example")


class SearchRequest(BaseModel):
    """Documentation search"""
    query: str = Field(..., description="Search query", min_length=1, max_length=200)
    category: Optional[str] = Field(None, description="Filter by category")
    language: Optional[ProgrammingLanguage] = Field(None, description="Filter by language")


class SearchResult(BaseModel):
    """Search result item"""
    result_type: str = Field(..., description="Type of result (guideline/practice)")
    title: str = Field(..., description="Result title")
    description: str = Field(..., description="Result description")
    relevance_score: float = Field(..., description="Relevance score", ge=0, le=1)


# Error Models
class ErrorResponse(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    type: str = Field(..., description="Exception type")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


# Success Models
class SuccessResponse(BaseModel):
    """Generic success response"""
    success: bool = Field(default=True, description="Operation success status")
    message: str = Field(..., description="Success message")
    data: Optional[Dict[str, Any]] = Field(None, description="Additional data")

# Made with Bob
