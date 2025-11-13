import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set required environment variables if not already set
if not os.getenv("REGION_ID"):
    os.environ["REGION_ID"] = "us-west-2"
if not os.getenv("MEMORY_ID"):
    os.environ["MEMORY_ID"] = "agentcore_starter_strands_mem-Aq6zOCGjAL"
if not os.getenv("MODEL_ID"):
    os.environ["MODEL_ID"] = "anthropic.claude-3-5-haiku-20241022-v1:0"

from agentcore_starter_strands import invoke

payload = {"prompt": "Hello, world"}

class Context:
    session_id = "local-test-session"

print(invoke(payload, Context()))
