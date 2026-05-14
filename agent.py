from google.genai import types
from call_function import available_functions, call_function
from prompts import system_prompt


def generate_content(client, messages, verbose=False):
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
    if verbose:
        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
    
    function_results_list = []

    # Handle Function Calls
    if response.function_calls:


        for function_call in response.function_calls:

            function_call_result = call_function(function_call, verbose)

            if not function_call_result.parts:
                raise Exception(f'Error occurred: {Exception}')
            
            response_property = function_call_result.parts[0].function_response
            if not response_property:
                raise Exception(f'Error occurred: {Exception}')

            response_field = response_property.response
            if not response_field:
                raise Exception(f'Error occurred: {Exception}')

            function_results_list.append(function_call_result.parts[0])

            if verbose:
                print(f"-> {response_field}")

    # Return results

    return response, function_results_list