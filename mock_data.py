"""
Mock data for DevAssist API development and testing
"""
from datetime import datetime, timedelta
from typing import List, Optional, Dict
import uuid
from models import (
    ReviewResponse, ReviewStatus, ProgrammingLanguage, Comment,
    IssueSeverity, AnalysisResult, CodeMetrics, Issue,
    GuidelineResponse, Rule, BestPractice
)


# Mock Reviews Storage
MOCK_REVIEWS: Dict[str, ReviewResponse] = {}


# Initialize some sample reviews
def _initialize_mock_reviews():
    """Initialize mock reviews data"""
    sample_reviews = [
        {
            "review_id": "rev-001",
            "title": "User Authentication Module Review",
            "status": ReviewStatus.COMPLETED,
            "language": ProgrammingLanguage.PYTHON,
            "code": """def authenticate_user(username, password):
    user = db.get_user(username)
    if user and user.password == password:
        return user
    return None""",
            "description": "Review authentication logic for security issues",
            "comments": [
                Comment(
                    comment_id="cmt-001",
                    line_number=3,
                    message="Password comparison should use secure hashing, not plain text",
                    severity=IssueSeverity.CRITICAL,
                    author="DevAssist",
                    created_at=datetime.utcnow() - timedelta(hours=2)
                ),
                Comment(
                    comment_id="cmt-002",
                    line_number=2,
                    message="Consider adding rate limiting to prevent brute force attacks",
                    severity=IssueSeverity.WARNING,
                    author="DevAssist",
                    created_at=datetime.utcnow() - timedelta(hours=1)
                )
            ],
            "created_at": datetime.utcnow() - timedelta(days=1),
            "updated_at": datetime.utcnow() - timedelta(hours=1)
        },
        {
            "review_id": "rev-002",
            "title": "API Rate Limiter Implementation",
            "status": ReviewStatus.IN_PROGRESS,
            "language": ProgrammingLanguage.JAVASCRIPT,
            "code": """const rateLimiter = (req, res, next) => {
    const key = req.ip;
    const limit = 100;
    // TODO: Implement rate limiting logic
    next();
};""",
            "description": "Review rate limiting implementation",
            "comments": [
                Comment(
                    comment_id="cmt-003",
                    line_number=4,
                    message="Consider using Redis for distributed rate limiting",
                    severity=IssueSeverity.INFO,
                    author="DevAssist",
                    created_at=datetime.utcnow() - timedelta(minutes=30)
                )
            ],
            "created_at": datetime.utcnow() - timedelta(hours=5),
            "updated_at": datetime.utcnow() - timedelta(minutes=30)
        },
        {
            "review_id": "rev-003",
            "title": "Database Query Optimization",
            "status": ReviewStatus.PENDING,
            "language": ProgrammingLanguage.PYTHON,
            "code": """def get_user_posts(user_id):
    posts = []
    for post in Post.objects.all():
        if post.user_id == user_id:
            posts.append(post)
    return posts""",
            "description": "Optimize database queries",
            "comments": [],
            "created_at": datetime.utcnow() - timedelta(minutes=15),
            "updated_at": datetime.utcnow() - timedelta(minutes=15)
        }
    ]
    
    for review_data in sample_reviews:
        review = ReviewResponse(**review_data)
        MOCK_REVIEWS[review.review_id] = review


# Initialize on module load
_initialize_mock_reviews()


# Mock Data Helper Functions
def get_review_by_id(review_id: str) -> Optional[ReviewResponse]:
    """Get a review by ID"""
    return MOCK_REVIEWS.get(review_id)


def get_all_reviews() -> List[ReviewResponse]:
    """Get all reviews"""
    return list(MOCK_REVIEWS.values())


def create_mock_review(title: str, code: str, language: ProgrammingLanguage, description: Optional[str] = None) -> ReviewResponse:
    """Create a new mock review"""
    review_id = f"rev-{uuid.uuid4().hex[:8]}"
    review = ReviewResponse(
        review_id=review_id,
        title=title,
        status=ReviewStatus.PENDING,
        language=language,
        code=code,
        description=description,
        comments=[],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    MOCK_REVIEWS[review_id] = review
    return review


def add_comment_to_review(review_id: str, line_number: int, message: str, severity: IssueSeverity) -> Optional[Comment]:
    """Add a comment to a review"""
    review = MOCK_REVIEWS.get(review_id)
    if not review:
        return None
    
    comment = Comment(
        comment_id=f"cmt-{uuid.uuid4().hex[:8]}",
        line_number=line_number,
        message=message,
        severity=severity,
        author="DevAssist",
        created_at=datetime.utcnow()
    )
    review.comments.append(comment)
    review.updated_at = datetime.utcnow()
    return comment


def get_mock_analysis_result(code: str, language: ProgrammingLanguage) -> AnalysisResult:
    """Generate mock analysis result"""
    # Simple mock logic based on code length
    lines = code.split('\n')
    loc = len([line for line in lines if line.strip()])
    
    # Mock complexity calculation
    complexity = min(100, loc * 2)
    
    # Mock issues
    issues = []
    if loc > 50:
        issues.append(Issue(
            line_number=1,
            message="Function is too long. Consider breaking it into smaller functions.",
            severity=IssueSeverity.WARNING,
            rule_id="complexity-001"
        ))
    
    if "password" in code.lower() and "==" in code:
        issues.append(Issue(
            line_number=code.lower().find("password") // 50 + 1,
            message="Avoid plain text password comparison. Use secure hashing.",
            severity=IssueSeverity.CRITICAL,
            rule_id="security-001"
        ))
    
    # Mock metrics
    metrics = CodeMetrics(
        lines_of_code=loc,
        cyclomatic_complexity=min(20, loc // 5 + 1),
        maintainability_index=max(0, 100 - complexity),
        comment_ratio=0.15
    )
    
    # Mock suggestions
    suggestions = [
        "Add docstrings to improve code documentation",
        "Consider adding type hints for better code clarity",
        "Add unit tests to ensure code reliability"
    ]
    
    return AnalysisResult(
        complexity_score=complexity,
        issues=issues,
        metrics=metrics,
        suggestions=suggestions,
        analyzed_at=datetime.utcnow()
    )


# Mock Guidelines Data
MOCK_GUIDELINES = {
    "python": GuidelineResponse(
        category="Python Best Practices",
        language=ProgrammingLanguage.PYTHON,
        rules=[
            Rule(
                rule_id="py-001",
                title="Use Type Hints",
                description="Always use type hints for function parameters and return values",
                examples=[
                    "def greet(name: str) -> str:\n    return f'Hello, {name}!'"
                ]
            ),
            Rule(
                rule_id="py-002",
                title="Follow PEP 8",
                description="Adhere to PEP 8 style guide for Python code",
                examples=[
                    "# Good: snake_case for variables\nuser_name = 'John'\n\n# Bad: camelCase\nuserName = 'John'"
                ]
            ),
            Rule(
                rule_id="py-003",
                title="Use Context Managers",
                description="Use 'with' statement for resource management",
                examples=[
                    "with open('file.txt', 'r') as f:\n    content = f.read()"
                ]
            )
        ]
    ),
    "javascript": GuidelineResponse(
        category="JavaScript Best Practices",
        language=ProgrammingLanguage.JAVASCRIPT,
        rules=[
            Rule(
                rule_id="js-001",
                title="Use const and let",
                description="Prefer const and let over var for variable declarations",
                examples=[
                    "const MAX_SIZE = 100;\nlet counter = 0;"
                ]
            ),
            Rule(
                rule_id="js-002",
                title="Use Arrow Functions",
                description="Use arrow functions for concise function expressions",
                examples=[
                    "const double = (x) => x * 2;"
                ]
            )
        ]
    )
}


def get_guidelines(language: Optional[ProgrammingLanguage] = None) -> GuidelineResponse:
    """Get coding guidelines"""
    if language and language.value in MOCK_GUIDELINES:
        return MOCK_GUIDELINES[language.value]
    
    # Return general guidelines
    return GuidelineResponse(
        category="General Best Practices",
        rules=[
            Rule(
                rule_id="gen-001",
                title="Write Clean Code",
                description="Keep code simple, readable, and maintainable",
                examples=["# Use meaningful variable names\nuser_count = 10  # Good\nx = 10  # Bad"]
            ),
            Rule(
                rule_id="gen-002",
                title="Add Comments",
                description="Document complex logic with clear comments",
                examples=["# Calculate compound interest\nresult = principal * (1 + rate) ** time"]
            )
        ]
    )


# Mock Best Practices Data
MOCK_BEST_PRACTICES = [
    BestPractice(
        practice_id="bp-001",
        title="Error Handling",
        description="Always handle errors gracefully and provide meaningful error messages",
        category="Error Management",
        language=ProgrammingLanguage.PYTHON,
        code_example="""try:
    result = risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise"""
    ),
    BestPractice(
        practice_id="bp-002",
        title="Input Validation",
        description="Validate all user inputs to prevent security vulnerabilities",
        category="Security",
        code_example="""def process_user_input(data):
    if not isinstance(data, str):
        raise ValueError("Input must be a string")
    if len(data) > MAX_LENGTH:
        raise ValueError("Input too long")
    return sanitize(data)"""
    ),
    BestPractice(
        practice_id="bp-003",
        title="Async/Await Pattern",
        description="Use async/await for non-blocking I/O operations",
        category="Performance",
        language=ProgrammingLanguage.JAVASCRIPT,
        code_example="""async function fetchData() {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch failed:', error);
    }
}"""
    )
]


def get_best_practices(language: Optional[ProgrammingLanguage] = None) -> List[BestPractice]:
    """Get best practices"""
    if language:
        return [bp for bp in MOCK_BEST_PRACTICES if bp.language == language or bp.language is None]
    return MOCK_BEST_PRACTICES


def search_documentation(query: str, category: Optional[str] = None, language: Optional[ProgrammingLanguage] = None) -> List[Dict]:
    """Search documentation"""
    results = []
    query_lower = query.lower()
    
    # Search in guidelines
    for lang_key, guideline in MOCK_GUIDELINES.items():
        if language and guideline.language != language:
            continue
        for rule in guideline.rules:
            if query_lower in rule.title.lower() or query_lower in rule.description.lower():
                results.append({
                    "result_type": "guideline",
                    "title": rule.title,
                    "description": rule.description,
                    "relevance_score": 0.9
                })
    
    # Search in best practices
    for practice in MOCK_BEST_PRACTICES:
        if language and practice.language and practice.language != language:
            continue
        if category and practice.category.lower() != category.lower():
            continue
        if query_lower in practice.title.lower() or query_lower in practice.description.lower():
            results.append({
                "result_type": "best_practice",
                "title": practice.title,
                "description": practice.description,
                "relevance_score": 0.85
            })
    
    return results

# Made with Bob
