# AgentCore PR Review Assistant

An AI-powered code review assistant built with AWS AgentCore that automatically analyzes GitHub pull requests for security vulnerabilities, code quality issues, and best practices.

## Features

- **Security Analysis**: Detects hardcoded credentials, injection vulnerabilities, authentication issues
- **Code Quality Review**: Assesses readability, complexity, naming conventions
- **Performance Optimization**: Identifies bottlenecks and inefficiencies
- **Best Practices**: Ensures framework/language conventions
- **Actionable Feedback**: Provides specific improvement recommendations with code examples

## Setup

### 1. Environment Variables

Create a `.env` file with:

```bash
# AWS Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
REGION_ID=us-west-2

# AgentCore Configuration
MEMORY_ID=your_memory_id
MODEL_ID=anthropic.claude-3-5-haiku-20241022-v1:0

# GitHub Integration (for webhook)
GITHUB_TOKEN=your_github_token
AGENTCORE_RUNTIME_ARN=your_agentcore_runtime_arn
```

### 2. Deploy AgentCore Agent

```bash
# Install dependencies
pip install -r requirements.txt

# Deploy to AWS
agentcore launch --auto-update-on-conflict \
  --env AWS_ACCESS_KEY_ID=your_key \
  --env AWS_SECRET_ACCESS_KEY=your_secret \
  --env REGION_ID=us-west-2 \
  --env MEMORY_ID=your_memory_id \
  --env MODEL_ID=anthropic.claude-3-5-haiku-20241022-v1:0
```

### 3. Test Locally

```bash
# Test general assistant
python test_invoke.py

# Test PR review functionality
python test_pr_review.py
```

### 4. GitHub Integration (Optional)

Deploy `github_webhook.py` as an AWS Lambda function and configure GitHub webhooks to automatically review PRs.

## Usage

### Direct Invocation

```bash
# General query
agentcore invoke '{"prompt": "Hello"}'

# PR Review
agentcore invoke '{"pr_data": {"title": "Fix auth bug", "author": "dev", "files": [...]}}'
```

### API Response

```json
{
  "review": "## PR Review Summary\n- Overall assessment\n- Key concerns\n...",
  "pr_title": "Fix auth bug",
  "files_reviewed": 3
}
```

## Architecture

- **AgentCore Runtime**: Hosts the AI agent with code execution capabilities
- **Claude 3.5 Haiku**: Provides intelligent code analysis
- **Memory Integration**: Maintains context across reviews
- **GitHub Webhook**: Automates PR review process

## Security

- No hardcoded credentials in source code
- Environment variables for sensitive configuration
- AWS IAM roles for secure access
- GitHub token for API authentication

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License
