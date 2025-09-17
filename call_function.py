from google.genai import types

def call_function(function_call_part, verbose=False):
    from functions.get_files_info import get_files_info
    from functions.get_file_content import get_file_content
    from functions.write_file import write_file
    from functions.run_python_file import run_python_file

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file
    }

    function_name = function_call_part.name
    kwargs = dict(function_call_part.args or {})

    kwargs["working_directory"] = "./calculator"

    func = function_map.get(function_name)
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"}
                )
            ]
        )
    
    result = func(**kwargs)
    # python
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result}
            )
        ]
    )