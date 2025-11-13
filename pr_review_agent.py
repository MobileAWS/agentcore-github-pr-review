"""
PR Review Assistant - AgentCore agent for automated code review
"""

import boto3
import os
import json
from dotenv import load_dotenv
from strands import Agent
from strands_tools.code_interpreter import AgentCoreCodeInterpreter
from bedrock_agentcore.memory.integrations.strands.config import AgentCoreMemoryConfig, RetrievalConfig
from bedrock_agentcore.memory.integrations.strands.session_manager import AgentCoreMemorySessionManager
from bedrock_agentcore.runtime import BedrockAgentCoreApp

load_dotenv()

# Get environment variables
MEMORY_ID = os.getenv("MEMORY_ID")
MODEL_ID = os.getenv("MODEL_ID")
REGION_ID = os.getenv("REGION_ID")

app = BedrockAgentCoreApp()

@app.entrypoint
def review_pr(payload, context):
    """
    Analyze a GitHub PR and provide review feedback
    Expected payload: {
        "pr_data": {
            "title": "PR title",
            "description": "PR description", 
            "files": [{"filename": "file.py", "patch": "diff content"}],
            "author": "username"
        }
    }
    """
    
    session_id = getattr(context, "session_id", None)
    session_manager = None

    if MEMORY_ID:
        memory_config = AgentCoreMemoryConfig(
            memory_id=MEMORY_ID,
            session_id=session_id or 'default',
            actor_id="pr_reviewer",
            region=REGION_ID,
            retrieval_config={
                "/reviews/patterns": RetrievalConfig(top_k=5, relevance_score=0.7),
                "/reviews/standards": RetrievalConfig(top_k=3, relevance_score=0.8),
            }
        )
        session_manager = AgentCoreMemorySessionManager(memory_config, REGION_ID)

    code_interpreter = AgentCoreCodeInterpreter(
        region=REGION_ID,
        session_name=session_id,
        auto_create=True
    )
    
    agent = Agent(
        model=MODEL_ID,
        tools=[code_interpreter.code_interpreter],
        session_manager=session_manager,
        system_prompt="""You are an expert code reviewer for a software development team. 

Your job is to analyze pull requests and provide constructive feedback on:
- Security vulnerabilities and potential exploits
- Code quality and maintainability issues  
- Performance concerns and optimization opportunities
- Adherence to coding standards and best practices
- Logic errors and edge cases
- Test coverage gaps

For each file changed, provide:
1. **Security Review**: Check for common vulnerabilities (SQL injection, XSS, auth issues, etc.)
2. **Code Quality**: Assess readability, complexity, naming conventions
3. **Performance**: Identify potential bottlenecks or inefficiencies
4. **Best Practices**: Ensure following language/framework conventions
5. **Suggestions**: Specific, actionable improvement recommendations

Use the code interpreter to analyze code patterns, run static analysis, or test logic when helpful.

Format your response as:
## PR Review Summary
- Overall assessment
- Key concerns (if any)
- Approval recommendation

## File-by-File Analysis
### filename.ext
- Issues found
- Suggestions
- Code snippets (if helpful)

Be thorough but constructive. Focus on helping the developer improve."""
    )
    
    pr_data = payload.get("pr_data", {})
    
    # Format PR data for analysis
    pr_context = f"""
PR Title: {pr_data.get('title', 'N/A')}
Author: {pr_data.get('author', 'N/A')}
Description: {pr_data.get('description', 'N/A')}

Files Changed ({len(pr_data.get('files', []))} files):
"""
    
    for file_data in pr_data.get('files', []):
        pr_context += f"\n--- {file_data.get('filename', 'unknown')} ---\n"
        pr_context += file_data.get('patch', 'No diff available')
        pr_context += "\n"
    
    prompt = f"Please review this pull request:\n\n{pr_context}"
    
    results = agent(prompt)
    return {
        "review": results.message.get('content', [{}])[0].get('text', str(results)),
        "pr_title": pr_data.get('title'),
        "files_reviewed": len(pr_data.get('files', []))
    }

if __name__ == "__main__":
    app.run()
