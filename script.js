// Tab Switching Functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
});

function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

function switchTab(tabName) {
    // Remove active class from all tabs and buttons
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => button.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    // Add active class to selected tab and button
    const selectedButton = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedContent = document.getElementById(tabName);
    
    if (selectedButton && selectedContent) {
        selectedButton.classList.add('active');
        selectedContent.classList.add('active');
    }
}

// Loading Overlay Functions
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Code Review Functions
async function submitReview() {
    const repo = document.getElementById('review-repo').value;
    const code = document.getElementById('review-code').value;
    const language = document.getElementById('review-language').value;
    
    // Validation
    if (!code.trim()) {
        alert('Please enter code to review');
        return;
    }
    
    if (!language) {
        alert('Please select a programming language');
        return;
    }
    
    showLoading();
    
    try {
        // Make actual API call to backend
        const response = await fetch('http://localhost:8000/api/review/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'dev-key-123' // Use your actual API key
            },
            body: JSON.stringify({
                title: repo || 'Code Review',
                code: code,
                language: language,
                description: 'Code review submission'
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        displayReviewResults(data);
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Error submitting review: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayReviewResults(data) {
    const resultsContainer = document.getElementById('review-results');
    const resultsContent = resultsContainer.querySelector('.results-content');
    
    // Check if AI analysis is available
    if (data.ai_analysis) {
        const analysis = data.ai_analysis;
        
        // Format the results with AI analysis
        let formattedResults = `AI-Powered Code Review Results
${'='.repeat(50)}

Language: ${data.language}
Review ID: ${data.review_id}
Status: ${data.status}

QUALITY SCORE: ${analysis.quality_score}/100
${'='.repeat(50)}

SUMMARY:
${analysis.summary}

ISSUES FOUND (${analysis.issues.length}):
${analysis.issues.length > 0 ? analysis.issues.map((issue, index) => `
${index + 1}. [${issue.severity}] ${issue.message}
   Line: ${issue.line || 'General'}
   Suggestion: ${issue.suggestion}
`).join('\n') : 'No issues found! Great job!'}

SUGGESTIONS FOR IMPROVEMENT (${analysis.suggestions.length}):
${analysis.suggestions.map((suggestion, index) => `${index + 1}. ${suggestion}`).join('\n')}

${'='.repeat(50)}
Powered by: ${analysis.powered_by}
`;
        
        resultsContent.textContent = formattedResults;
    } else {
        // Fallback format if no AI analysis
        let formattedResults = `Code Review Results
${'='.repeat(50)}

Language: ${data.language}
Review ID: ${data.review_id}
Status: ${data.status}
Lines of Code: ${data.code.split('\n').length}

Review created successfully!
`;
        resultsContent.textContent = formattedResults;
    }
    
    resultsContainer.style.display = 'block';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Repository Analysis Functions
async function submitAnalysis() {
    const repo = document.getElementById('analysis-repo').value;
    const branch = document.getElementById('analysis-branch').value || 'main';
    const includeMetrics = document.getElementById('include-metrics').checked;
    const includeDependencies = document.getElementById('include-dependencies').checked;
    const includeStructure = document.getElementById('include-structure').checked;
    
    // Validation
    if (!repo.trim()) {
        alert('Please enter a repository URL');
        return;
    }
    
    showLoading();
    
    try {
        // Simulate API call
        const response = await simulateAPICall({
            endpoint: '/api/analyze',
            data: {
                repository: repo,
                branch: branch,
                options: {
                    metrics: includeMetrics,
                    dependencies: includeDependencies,
                    structure: includeStructure
                }
            }
        });
        
        displayAnalysisResults(response);
    } catch (error) {
        alert('Error analyzing repository: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayAnalysisResults(data) {
    const resultsContainer = document.getElementById('analysis-results');
    const resultsContent = resultsContainer.querySelector('.results-content');
    
    // Format the results
    let formattedResults = `Repository Analysis
${'='.repeat(50)}

Repository: ${data.repository}
Branch: ${data.branch}
Last Updated: ${data.lastUpdated}

Project Statistics:
- Total Files: ${data.stats.totalFiles}
- Total Lines: ${data.stats.totalLines}
- Languages: ${data.stats.languages.join(', ')}
- Contributors: ${data.stats.contributors}

${data.metrics ? `
Code Metrics:
- Maintainability Index: ${data.metrics.maintainability}/100
- Cyclomatic Complexity: ${data.metrics.complexity}
- Code Duplication: ${data.metrics.duplication}%
- Test Coverage: ${data.metrics.coverage}%
` : ''}

${data.dependencies ? `
Dependencies:
${data.dependencies.map(dep => `- ${dep.name} (${dep.version})`).join('\n')}
` : ''}

${data.structure ? `
Project Structure:
${data.structure.map(item => `${item.indent}${item.name}`).join('\n')}
` : ''}

${'='.repeat(50)}
Powered by: IBM Bob + Gemini AI
`;
    
    resultsContent.textContent = formattedResults;
    resultsContainer.style.display = 'block';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Documentation Generation Functions
async function generateDocs() {
    const repo = document.getElementById('docs-repo').value;
    const code = document.getElementById('review-code').value; // Reuse code from review tab
    const type = document.getElementById('docs-type').value;
    const format = document.getElementById('docs-format').value;
    const language = document.getElementById('review-language').value || 'python';
    
    // Validation
    if (!code.trim()) {
        alert('Please enter code in the Code Review tab first');
        return;
    }
    
    showLoading();
    
    try {
        // Make actual API call to backend
        const response = await fetch('http://localhost:8000/api/docs/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-Key': 'dev-key-123' // Use your actual API key
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const data = await response.json();
        displayDocsResults(data, type);
    } catch (error) {
        console.error('Error generating documentation:', error);
        alert('Error generating documentation: ' + error.message);
    } finally {
        hideLoading();
    }
}

function displayDocsResults(data, type) {
    const resultsContainer = document.getElementById('docs-results');
    const resultsContent = resultsContainer.querySelector('.results-content');
    
    // Format the results based on type
    let formattedResults = '';
    
    if (type === 'readme') {
        formattedResults = `# AI-Generated README Section
${'='.repeat(50)}

${data.readme_section}

## Plain English Explanation
${data.plain_english}

## Parameters
${data.parameters && data.parameters.length > 0 ? 
    data.parameters.map(p => `- **${p.name}** (${p.type}): ${p.description}`).join('\n') : 
    'No parameters'}

## Returns
${data.returns}

## Usage Examples
${data.examples && data.examples.length > 0 ? 
    data.examples.map((ex, i) => `### Example ${i + 1}\n\`\`\`\n${ex}\n\`\`\``).join('\n\n') : 
    'No examples available'}

${'='.repeat(50)}
Powered by: ${data.powered_by}
`;
    } else if (type === 'api') {
        formattedResults = `# API Documentation
${'='.repeat(50)}

## Docstring
${data.docstring}

## Plain English Description
${data.plain_english}

## Parameters
${data.parameters && data.parameters.length > 0 ? 
    data.parameters.map(p => `- **${p.name}** (${p.type}): ${p.description}`).join('\n') : 
    'No parameters'}

## Returns
${data.returns}

## Examples
${data.examples && data.examples.length > 0 ? 
    data.examples.map((ex, i) => `${i + 1}. ${ex}`).join('\n') : 
    'No examples available'}

${'='.repeat(50)}
Powered by: ${data.powered_by}
`;
    } else {
        formattedResults = `# Generated Documentation
${'='.repeat(50)}

## Docstring
${data.docstring}

## Plain English Explanation
${data.plain_english}

## README Section
${data.readme_section}

${'='.repeat(50)}
Powered by: ${data.powered_by}
`;
    }
    
    resultsContent.textContent = formattedResults;
    resultsContainer.style.display = 'block';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function downloadDocs() {
    const resultsContent = document.querySelector('#docs-results .results-content');
    const format = document.getElementById('docs-format').value;
    const content = resultsContent.textContent;
    
    // Create blob and download
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `documentation.${format === 'markdown' ? 'md' : format}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Simulate API Call (Mock Function for analysis - kept for backward compatibility)
function simulateAPICall({ endpoint, data }) {
    return new Promise((resolve) => {
        setTimeout(() => {
            // Mock responses based on endpoint
            if (endpoint === '/api/analyze') {
                resolve({
                    repository: data.repository,
                    branch: data.branch,
                    lastUpdated: new Date().toISOString().split('T')[0],
                    stats: {
                        totalFiles: Math.floor(Math.random() * 100) + 50,
                        totalLines: Math.floor(Math.random() * 10000) + 5000,
                        languages: ['Python', 'JavaScript', 'HTML', 'CSS'],
                        contributors: Math.floor(Math.random() * 10) + 3
                    },
                    metrics: data.options.metrics ? {
                        maintainability: Math.floor(Math.random() * 30) + 65,
                        complexity: Math.floor(Math.random() * 5) + 3,
                        duplication: Math.floor(Math.random() * 15) + 5,
                        coverage: Math.floor(Math.random() * 40) + 50
                    } : null,
                    dependencies: data.options.dependencies ? [
                        { name: 'flask', version: '2.3.0' },
                        { name: 'requests', version: '2.31.0' },
                        { name: 'pytest', version: '7.4.0' }
                    ] : null,
                    structure: data.options.structure ? [
                        { indent: '', name: '📁 src/' },
                        { indent: '  ', name: '📄 main.py' },
                        { indent: '  ', name: '📄 config.py' },
                        { indent: '  ', name: '📁 routes/' },
                        { indent: '    ', name: '📄 __init__.py' },
                        { indent: '    ', name: '📄 review.py' }
                    ] : null
                });
            }
        }, 1500); // Simulate network delay
    });
}

// Made with Bob
