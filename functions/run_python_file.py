import os
import subprocess
import sys 
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_target = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([abs_working, abs_target]) != abs_working:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(abs_target):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        exc_list = [sys.executable, abs_target] + args
        result = subprocess.run(exc_list, cwd=working_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30, check=False)
        out = result.stdout or ""
        err = result.stderr or ""
        code = result.returncode

        if out.strip() == "" and err.strip() == "":
            return "No output produced."
        else:
            lines = []
            if out.strip():
                lines.append(f"STDOUT: {out.strip()}")
            if err.strip():
                lines.append(f"STDERR: {err.strip()}")
            if code != 0:
                lines.append(f"Process exited with code {code}")
            return "\n".join(lines)

    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="executes a specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="the path to the file to be executed"
            )
        }
    )
)