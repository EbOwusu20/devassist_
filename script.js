// Configuration
const API_CONFIG = {
    baseURL: 'https://devassist-api-6klc.onrender.com/api',
    timeout: 30000
};

const MOCK_API_DELAY = 1500;

// Utility Functions
/**
 * Sanitizes user input to prevent XSS attacks
 * @param {string} input - The input string to sanitize
 * @returns {string} Sanitized string
 */
function sanitizeInput(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
}

/**
 * Validates input based on type
 * @param {string} value - The value to validate
 * @param {string} type - The type of validation ('url', 'code', 'text')
 * @returns {boolean} True if valid
 */
function validateInput(value, type) {
    if (!value?.trim()) return false;
    
    switch(type) {
        case 'url':
            return /^https?:\/\/.+/.test(value);
        case 'code':
            return value.trim().length > 0;
        case 'text':
            return value.trim().length > 0;
        default:
            return true;
    }
}

/**
 * Shows a notification to the user
 * @param {string} message - The message to display
 * @param {string} type - The type of notification ('success', 'error', 'warning', 'info')
 */
function showNotification(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 5px;
            color: white;
            font-weight: 500;
            z-index: 10000;
            max-width: 400px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            animation: slideIn 0.3s ease-out;
        `;
        document.body.appendChild(notification);
    }
    
    // Set color based on type
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    
    notification.style.backgroundColor = colors[type] || colors.info;
    notification.textContent = message;
    notification.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 5000);
}

/**
 * Handles API errors consistently
 * @param {Error} error - The error object
 * @param {string} context - Context of where the error occurred
 */
function handleAPIError(error, context) {
    console.error(`Error in ${context}:`, error);
    
    let message = `Failed to ${context}. `;
    if (error.message.includes('API error')) {
        message += 'Server returned an error. Please try again later.';
    } else if (error.message.includes('Failed to fetch')) {
        message += 'Network error. Please check your connection.';
    } else {
        message += error.message;
    }
    
    showNotification(message, 'error');
}

/**
 * Makes an authenticated API call
 * @param {string} endpoint - The API endpoint
 * @param {Object} data - The data to send
 * @returns {Promise<Object>} The API response
 */
async function makeAPICall(endpoint, data) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), API_CONFIG.timeout);
    
    try {
        const response = await fetch(`${API_CONFIG.baseURL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
                // API key should be handled by backend session/authentication
                // Never expose API keys in frontend code
            },
            body: JSON.stringify(data),
            signal: controller.signal
        });
        
        clearTimeout(timeoutId);
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status} ${response.statusText}`);
        }
        
        return await response.json();
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout. Please try again.');
        }
        throw error;
    }
}

/**
 * Displays results in a container with smooth scrolling
 * @param {string} containerId - The ID of the results container
 * @param {string} content - The formatted content to display
 */
function displayResults(containerId, content) {
    const resultsContainer = document.getElementById(containerId);
    const resultsContent = resultsContainer.querySelector('.results-content');
    
    resultsContent.textContent = content;
    resultsContainer.style.display = 'block';
    
    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Tab Switching Functionality
document.addEventListener('DOMContentLoaded', function() {
    initializeTabs();
    addKeyboardShortcuts();
});

/**
 * Initializes tab switching functionality
 */
function initializeTabs() {
    const tabButtons = document.querySelectorAll('.tab-button');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });
}

/**
 * Switches to a specific tab
 * @param {string} tabName - The name of the tab to switch to
 */
function switchTab(tabName) {
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => button.classList.remove('active'));
    tabContents.forEach(content => content.classList.remove('active'));
    
    const selectedButton = document.querySelector(`[data-tab="${tabName}"]`);
    const selectedContent = document.getElementById(tabName);
    
    if (selectedButton && selectedContent) {
        selectedButton.classList.add('active');
        selectedContent.classList.add('active');
    }
}

/**
 * Adds keyboard shortcuts for better accessibility
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Alt + 1/2/3 for tab switching
        if (e.altKey && e.key >= '1' && e.key <= '3') {
            e.preventDefault();
            const tabs = ['code-review', 'repo-analysis', 'docs-generation'];
            switchTab(tabs[parseInt(e.key) - 1]);
        }
    });
}

// Loading Overlay Functions
/**
 * Shows the loading overlay
 */
function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex';
}

/**
 * Hides the loading overlay
 */
function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none';
}

// Code Review Functions
/**
 * Submits code for review
 */
async function submitReview() {
    const repo = document.getElementById('review-repo').value;
    const code = document.getElementById('review-code').value;
    const language = document.getElementById('review-language').value;
    
    // Validation
    if (!validateInput(code, 'code')) {
        showNotification('Please enter code to review', 'warning');
        return;
    }
    
    if (!language) {
        showNotification('Please select a programming language', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        const data = await makeAPICall('/review/submit', {
            title: sanitizeInput(repo) || 'Code Review',
            code: code, // Code is sent to backend for processing
            language: language,
            description: 'Code review submission'
        });
        
        displayReviewResults(data);
        showNotification('Code review completed successfully!', 'success');
    } catch (error) {
        handleAPIError(error, 'submit code review');
    } finally {
        hideLoading();
    }
}

/**
 * Displays code review results
 * @param {Object} data - The review data from API
 */
function displayReviewResults(data) {
    let formattedResults = '';
    
    if (data.ai_analysis) {
        const analysis = data.ai_analysis;
        
        formattedResults = `AI-Powered Code Review Results
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
    } else {
        formattedResults = `Code Review Results
${'='.repeat(50)}

Language: ${data.language}
Review ID: ${data.review_id}
Status: ${data.status}
Lines of Code: ${data.code.split('\n').length}

Review created successfully!
`;
    }
    
    displayResults('review-results', formattedResults);
}

// Repository Analysis Functions
/**
 * Submits repository for analysis
 */
async function submitAnalysis() {
    const repo = document.getElementById('analysis-repo').value;
    const branch = document.getElementById('analysis-branch').value || 'main';
    const includeMetrics = document.getElementById('include-metrics').checked;
    const includeDependencies = document.getElementById('include-dependencies').checked;
    const includeStructure = document.getElementById('include-structure').checked;
    
    // Validation
    if (!validateInput(repo, 'url')) {
        showNotification('Please enter a valid repository URL', 'warning');
        return;
    }
    
    showLoading();
    
    try {
        // Note: This currently uses mock data. Replace with real API when available
        const response = await simulateAPICall({
            endpoint: '/analyze',
            data: {
                repository: sanitizeInput(repo),
                branch: sanitizeInput(branch),
                options: {
                    metrics: includeMetrics,
                    dependencies: includeDependencies,
                    structure: includeStructure
                }
            }
        });
        
        displayAnalysisResults(response);
        showNotification('Repository analysis completed!', 'success');
    } catch (error) {
        handleAPIError(error, 'analyze repository');
    } finally {
        hideLoading();
    }
}

/**
 * Displays repository analysis results
 * @param {Object} data - The analysis data
 */
function displayAnalysisResults(data) {
    const formattedResults = `Repository Analysis
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
    
    displayResults('analysis-results', formattedResults);
}

// Documentation Generation Functions
/**
 * Generates documentation for code
 */
/**
 * Generates documentation for a GitHub repository
 */
async function generateDocs() {
    const repo = document.getElementById('docs-repo').value;
    const type = document.getElementById('docs-type').value;
    const format = document.getElementById('docs-format').value;
    const language = document.getElementById('review-language').value || 'python';

    // Validation
    if (!validateInput(repo, 'url')) {
        showNotification('Please enter a valid GitHub repository URL', 'warning');
        return;
    }

    showLoading();

    try {
        // Extract owner and repo name from GitHub URL
        // e.g. https://github.com/EbOwusu20/DevAssist
        const cleanUrl = repo.replace('https://github.com/', '').split('/');
        const owner = cleanUrl[0];
        const repoName = cleanUrl[1];

        if (!owner || !repoName) {
            showNotification('Please enter a valid GitHub URL like https://github.com/username/repository', 'warning');
            hideLoading();
            return;
        }

        // Step 1 — Try to fetch README from GitHub API
        let code = '';
        showNotification('Fetching repository from GitHub...', 'info');

        const githubRes = await fetch(
            `https://api.github.com/repos/${owner}/${repoName}/readme`,
            { headers: { Accept: 'application/vnd.github.v3.raw' } }
        );

        if (githubRes.ok) {
            // README found — use it
            code = await githubRes.text();
            showNotification('Repository fetched! Generating documentation...', 'info');
        } else {
            // No README — fallback to file structure
            showNotification('No README found. Fetching file structure...', 'info');

            const treeRes = await fetch(
                `https://api.github.com/repos/${owner}/${repoName}/git/trees/main?recursive=1`
            );

            if (treeRes.ok) {
                const treeData = await treeRes.json();
                const fileList = treeData.tree
                    .map(f => f.path)
                    .join('\n');
                code = `Repository: ${repo}\n\nFile Structure:\n${fileList}`;
            } else {
                // Try master branch instead of main
                const masterRes = await fetch(
                    `https://api.github.com/repos/${owner}/${repoName}/git/trees/master?recursive=1`
                );

                if (masterRes.ok) {
                    const masterData = await masterRes.json();
                    const fileList = masterData.tree
                        .map(f => f.path)
                        .join('\n');
                    code = `Repository: ${repo}\n\nFile Structure:\n${fileList}`;
                } else {
                    showNotification('Could not fetch repository. Make sure the URL is correct and the repo is public.', 'error');
                    hideLoading();
                    return;
                }
            }
        }

        // Step 2 — Send fetched content to backend for AI documentation
        const data = await makeAPICall('/docs/generate', {
            code: code,
            language: language
        });

        displayDocsResults(data, type);
        showNotification('Documentation generated successfully!', 'success');

    } catch (error) {
        handleAPIError(error, 'generate documentation');
    } finally {
        hideLoading();
    }
}

/**
 * Displays documentation generation results
 * @param {Object} data - The documentation data from API
 * @param {string} type - The type of documentation
 */
function displayDocsResults(data, type) {
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
    
    displayResults('docs-results', formattedResults);
}

/**
 * Downloads the generated documentation
 */
function downloadDocs() {
    const resultsContent = document.querySelector('#docs-results .results-content');
    const format = document.getElementById('docs-format').value;
    const content = resultsContent.textContent;
    
    if (!content) {
        showNotification('No documentation to download', 'warning');
        return;
    }
    
    try {
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `documentation.${format === 'markdown' ? 'md' : format}`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showNotification('Documentation downloaded successfully!', 'success');
    } catch (error) {
        handleAPIError(error, 'download documentation');
    }
}

// Mock API Function (for repository analysis until real API is implemented)
/**
 * Simulates an API call with mock data
 * @param {Object} params - Parameters containing endpoint and data
 * @returns {Promise<Object>} Mock response data
 */
function simulateAPICall({ endpoint, data }) {
    return new Promise((resolve) => {
        setTimeout(() => {
            if (endpoint === '/analyze') {
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
        }, MOCK_API_DELAY);
    });
}

// Made with Bob - Enhanced Edition
