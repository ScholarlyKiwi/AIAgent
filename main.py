import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse

def main():
    print("Hello from ai-agent-boot-dev!")

    client = load_ai_api()

    args = get_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    model = "gemini-2.5-flash"
    call_ai_test(client, model, messages, args)

def get_args():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    return args

def load_ai_api():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY not found in .env file")
    client = genai.Client(api_key=api_key)
    return client

def call_ai_test(client, model, contents, args):

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    response = client.models.generate_content(model=model, contents=contents)
    if response.usage_metadata == None:
        raise RuntimeError("GenAI failed to respond.")

    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    print(f"{response.text}")

if __name__ == "__main__":
    main()
