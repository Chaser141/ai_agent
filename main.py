import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) 
if len(sys.argv) < 2:
    print("Usage: uv run main.py your prompt")
    sys.exit(1)
prompt = sys.argv[1]
verbose = "--verbose" in sys.argv 
messages = types.Content(role="user", parts=[types.Part(text=prompt)])


def main():
    print("Hello from ai-agent!")
    
    response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages)
    
    usage = response.usage_metadata
    if verbose:
        
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    print(response.text)

if __name__ == "__main__":
    main()
