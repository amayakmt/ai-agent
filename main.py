import os, argparse, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from agent import generate_content
from config import MAX_ITERS

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

    # Print the executable prompt
    if verbose_arg:
        print(f'User prompt: {user_prompt}')

    # Store the conversation history
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    # Execute the agent
    for _ in range(MAX_ITERS):

        model_response, function_call_results = generate_content(client, messages, verbose_arg)

        for candidate in model_response.candidates:
            messages.append(candidate.content)

        messages.append(types.Content(role="user", parts=function_call_results))
        
        if not function_call_results:
            print(model_response.text)
            break
    
    else:
        print(f'Error: agent did not produce a final response within {MAX_ITERS} iterations.')
        sys.exit(1)

if __name__ == "__main__":
    main()