import os
import sys 
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_content
from functions.write_file import write_file, schema_write_file 
from functions.run_python_file import run_python_file, schema_run_python_file
from google.genai import types



load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) 
if len(sys.argv) < 2:
    print("Usage: uv run main.py your prompt")
    sys.exit(1)
prompt = sys.argv[1]
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- when writing files, extract the content to write from the user's request. Content is typically provided in quotes
- Execute Python files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
verbose = "--verbose" in sys.argv 
messages = types.Content(role="user", parts=[types.Part(text=prompt)])
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt    
)

def main():
    print("Hello from ai-agent!")
    
    response = client.models.generate_content(model = 'gemini-2.0-flash-001', contents = messages, 
                                              config=config)
    
    usage = response.usage_metadata
    if verbose:
        
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    if response.function_calls:
        for function_call_part in response.function_calls:
            print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(response.text)



if __name__ == "__main__":
    main()
