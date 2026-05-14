import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    # Load Gemini API
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY was not found.")

    # Connect Gemini AI Client
    client = genai.Client(api_key=api_key)

    # Parse Command Line Prompt
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")

    # Verbose Output
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    # Parse all the passed arguments in the command line
    args = parser.parse_args() 
    user_prompt = args.user_prompt # user input
    verbose_arg = args.verbose # verbose argument

    # Store the conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # Execute Gemini-2.5-Flash model
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0,
            tools=[available_functions]),
    )

    # Checks if the output contains usage_metadata (True if ran correctly)
    if not response.usage_metadata:
        raise RuntimeError('API request failed.')

    # Print the results
    if verbose_arg:
        print(f'User prompt: {user_prompt}')
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    if response.function_calls:

        function_results_list = []
        for function_call in response.function_calls:

            function_call_result = call_function(function_call, verbose_arg)

            if not function_call_result.parts:
                raise Exception(f'Error occurred: {Exception}')
            
            response_property = function_call_result.parts[0].function_response
            if not response_property:
                raise Exception(f'Error occurred: {Exception}')

            response_field = response_property.response
            if not response_field:
                raise Exception(f'Error occurred: {Exception}')

            function_results_list.extend(function_call_result.parts[0])

            if verbose_arg:
                print(f"-> {response_field}")

    else:
        print(response.text)

if __name__ == "__main__":
    main()