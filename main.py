import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import *
import pprint

def main():
    print("Hello from ai-agent-boot-dev!")

    client = load_ai_api()

    args = get_args()

    messages = args.user_prompt

    model = "gemini-2.5-flash"

    ai_results = call_generate_content(client, model, messages, args)

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

def call_generate_content(client, model, messages, args):

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    try:

        contents = [types.Content(role="user", parts=[types.Part(text=messages)])]

        while_counter = 0

        while while_counter <= 20:
            while_counter += 1

            response = client.models.generate_content(
                model=model, 
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    tools=[available_functions]),
            )

            if response.usage_metadata == None:
                raise RuntimeError("GenAI failed to respond.")

            if args.verbose:
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
           
            if not response.candidates == None:
                for candidate in response.candidates:
                    content = candidate.content
                    contents.append(content)

            if not response.function_calls:
                return response.text

            if response.function_calls != None:

                returned_function_results = list()

                if args.verbose:
                    print(f"function results = {response.function_calls}\n")

                for function_call in response.function_calls:
                    if args.verbose:
                        print(f"Calling function: {function_call.name}({function_call.args})\n")

                    function_call_result = call_function( function_call, args.verbose)
                    
                    if len(function_call_result.parts) == 0:
                        raise Exception(f"Error: no results from function call {function_call.name}({function_call.args})")

                    function_response = function_call_result.parts[0].function_response
                    if function_response == None:
                        raise Exception(f"Error: emtpy function response from function call {function_call.name}({function_call.args})")
                    if function_response.response == None:
                        raise Exception(f"Error: empty response from function call {function_call.name}({function_call.args})")
                    
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}\n")

                    returned_function_results.append(dict(function_call_result.parts[0]))

                results_content = types.Content(parts=returned_function_results, role='user')
                contents.append(results_content)

        return results_content
    except Exception as e:
            print(f"Error: calling AI {e}")

     


if __name__ == "__main__":
    main()
