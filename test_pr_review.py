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

# Sample PR data for testing
sample_pr = {
    "pr_data": {
        "title": "Add user authentication endpoint",
        "author": "developer123",
        "description": "Implements JWT-based authentication for the API",
        "files": [
            {
                "filename": "auth.py",
                "patch": """@@ -0,0 +1,25 @@
+import jwt
+from flask import request, jsonify
+
+def authenticate_user():
+    token = request.headers.get('Authorization')
+    if not token:
+        return jsonify({'error': 'No token provided'}), 401
+    
+    try:
+        # Decode JWT token
+        payload = jwt.decode(token, 'secret_key', algorithms=['HS256'])
+        user_id = payload['user_id']
+        return jsonify({'user_id': user_id}), 200
+    except jwt.ExpiredSignatureError:
+        return jsonify({'error': 'Token expired'}), 401
+    except jwt.InvalidTokenError:
+        return jsonify({'error': 'Invalid token'}), 401
+
+def login():
+    username = request.json.get('username')
+    password = request.json.get('password')
+    
+    # TODO: Add proper password validation
+    if username == 'admin' and password == 'password':
+        token = jwt.encode({'user_id': 1}, 'secret_key', algorithm='HS256')
+        return jsonify({'token': token}), 200
+    
+    return jsonify({'error': 'Invalid credentials'}), 401"""
            }
        ]
    }
}

class Context:
    session_id = "pr-review-test-session"

print("Testing PR Review Assistant...")
result = invoke(sample_pr, Context())
print("\n" + "="*50)
print("REVIEW RESULT:")
print("="*50)
print(result['review'])
