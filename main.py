import os
import sys
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()

    if len(sys.argv) < 2:
        print("Need to input a prompt.")
        exit(1)

    
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=sys.argv[1]
    )
    print(f"{response.text}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    

if __name__ == "__main__":
    main()