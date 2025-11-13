"""
Strand Agent sample with AgentCore 

python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
"""

import boto3
import os
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

print("AWS_ACCESS_KEY_ID present:", os.getenv("AWS_ACCESS_KEY_ID"))
print("AWS_SECRET_ACCESS_KEY present:", os.getenv("AWS_SECRET_ACCESS_KEY"))
print("MEMORY_ID present:", MEMORY_ID)
print("MODEL_ID present:", MODEL_ID)
print("REGION_ID present:", REGION_ID)

boto3.Session()

@app.entrypoint
def invoke( payload, context):
    actor_id = "quickstart_user"

    # Get runtime session ID for isolation 
    session_id = getattr(context, "session_id", None ) 

    session_manager = None

    if MEMORY_ID:
        memory_config = AgentCoreMemoryConfig(
            memory_id=MEMORY_ID,
            session_id=session_id or 'default',
            actor_id=actor_id,
            region=REGION_ID,
            retrieval_config={
                f"/users/{actor_id}/facts": RetrievalConfig(top_k=3, relevance_score=0.5),
                f"/users/{actor_id}/preferences": RetrievalConfig(top_k=3, relevance_score=0.5),
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
        system_prompt="""You are a helpful assistant with code execution capabilities. Use tools when appropriate.
        Response format when using code:
        1. Brief explanation of your approach
        2. Code block showing the executed code
        3. Results and analysis
        """
    )
    results = agent(payload.get("prompt", ""))
    return {"response": results.message.get('content', [{}])[0].get('text', str(results))}

if __name__ == "__main__":    
    app.run()

