import subprocess
import os
from rest_framework.response import Response
from rest_framework.decorators import api_view

CONFIG = {
    "python": {"ext": "py", "image": "python:3.12-slim", "command": "python"},
    "javascript": {"ext": "js", "image": "node:latest", "command": "node"},
    "php": {"ext": "php", "image": "php:latest", "command": "php"}
}

def run_code_in_docker(language, user_file_path, test_code):
    try:
        if language not in CONFIG:
            return {"success": False, "error": f"Unsupported language: {language}"}

        config = CONFIG[language]
        ext, image, command = config["ext"], config["image"], config["command"]

        current_dir = os.path.dirname(user_file_path).replace("\\", "/")
        temp_test_filename = os.path.join(current_dir, f"temp_test_script.{ext}")

        if not os.path.exists(user_file_path):
            return {"success": False, "error": f"File not found at {user_file_path}"}

        with open(user_file_path, "r") as user_file:
            user_code = user_file.read()

        full_code = f"{user_code}\n{test_code}"

        with open(temp_test_filename, "w") as temp_file:
            temp_file.write(full_code)

        result = subprocess.run(
            [
                "docker", "run", "--rm", "-v",
                f"{current_dir}:/app",
                image,
                command, f"/app/{os.path.basename(temp_test_filename)}"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        response = {"success": result.returncode == 0,
                    "output": result.stdout if result.returncode == 0 else result.stderr}

    except subprocess.TimeoutExpired:
        response = {"success": False, "error": "Execution timed out."}
    except Exception as e:
        response = {"success": False, "error": str(e)}
    finally:
        if os.path.exists(temp_test_filename):
            os.remove(temp_test_filename)

    return response

@api_view(["POST"])
def run_code(request):
    data = request.data
    language = data.get("language")
    user_file_path = data.get("file_path")
    test_code = data.get("test_code")

    if not all([language, user_file_path, test_code]):
        return Response({"success": False, "error": "Missing required parameters."}, status=400)

    result = run_code_in_docker(language, user_file_path, test_code)
    return Response(result)
