import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("Need to input a prompt.")
        exit(1)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = sys.argv[1]
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    If the user doesn't specify an exact filepath you should start by looking through the available files to understand which one it they are referring to. 
    If you don't find the file, you should call get_files_info on discovered directories to see what's inside and dig deeper.
    Don't assume that a file with a different name is the correct one until after you've looked through all subdirectories.
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    When you are finished you should no longer need to run any more functions.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)])
    ]

    verbose = False
    if len(sys.argv) == 3:
            if sys.argv[2] == "--verbose":
                verbose = True

    try:
        for i in range(20):
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                ),
            )
            
            prompt_tokens = response.usage_metadata.prompt_token_count
            response_tokens = response.usage_metadata.candidates_token_count

            if verbose:
                print("\nPrompt tokens:", prompt_tokens, "\n")
                print("Response tokens:", response_tokens, "\n")

            if response.function_calls:
                print(f"\nLoop number {i+1}\nCurrent thoughts:\n{response.text}\n")
                function_call_result = call_function(response.function_calls[0], verbose)
                print(f"-> {function_call_result.parts[0].function_response.response}")
                messages.append(response.candidates[0].content) 
                messages.append(types.Content(
                    role="user", 
                    parts=[types.Part(text=f"Here is the result of the previous function: {str(function_call_result.parts[0].function_response.response)}")]
                ))
            else:
                print(f"\nLoop number {i+1}\nFinal answer:\n{response.text}\n")
                return
            
            #print(f"\nTesting Messages output: {messages}")
            #print(f"\nCandidate text: {response.candidates[0].content.parts[0]}\n")
            #print(f"Response: {response.candidates[0].finish_message}")
    except Exception as e:
        print(f"Error {e}")

if __name__ == "__main__":
    main()