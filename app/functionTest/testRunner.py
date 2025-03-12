import subprocess
import os

def run_code_in_docker(language, user_file_path, test_code):
    try:
        file_extension = {"python": "py", "javascript": "js", "php": "php"}
        docker_images = {"python": "python:3.12-slim", "javascript": "node:latest", "php": "php:latest"}

        if language not in file_extension or language not in docker_images:
            return False, f"Unsupported language: {language}"

        ext = file_extension[language]

        current_dir = os.path.dirname(user_file_path).replace("\\", "/")
        temp_test_filename = os.path.join(current_dir, f"temp_test_script.{ext}")

        if not os.path.exists(user_file_path):
            return False, f"Error: File not found at {user_file_path}"

        with open(user_file_path, "r") as user_file:
            user_code = user_file.read()

        full_code = f"{user_code}\n{test_code}"

        with open(temp_test_filename, "w") as temp_file:
            temp_file.write(full_code)

        print(f"Temp file created at: {temp_test_filename}")

        result = subprocess.run(
            [
                "docker", "run", "--rm", "-v",
                f"{current_dir}:/app",
                docker_images[language],
                "node" if language == "javascript" else "python" if language == "python" else "php",
                f"/app/{os.path.basename(temp_test_filename)}"
            ],
            capture_output=True,
            text=True,
            timeout=30
        )

        print("Docker output:")
        print(result.stdout)

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Execution timed out."
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_test_filename):
            os.remove(temp_test_filename)
            print(f"Deleted temp file: {temp_test_filename}")


if __name__ == "__main__":
    # Pour Python
    user_file_path = os.path.join(os.getcwd(), "app", "functionTest", "user_file.py")

    test_code_python = """
result = add(2, 3)
expected = 5
assert result == expected, f"Test failed: expected {expected}, got {result}"
print("Test passed!")
"""

    success, output = run_code_in_docker("python", user_file_path, test_code_python)

    if success:
        print("Python tests succeeded! Output:")
        print(output)
    else:
        print("Python tests failed! Error:")
        print(output)

    # Pour JavaScript
    user_file_path = os.path.join(os.getcwd(), "app", "functionTest", "user_file.js")

    test_code_js = """
const result = add(2, 3);
const expected = 5;
if (result !== expected) {
    console.log(`Test failed: expected ${expected}, got ${result}`);
} else {
    console.log("Test passed!");
}
"""

    success, output = run_code_in_docker("javascript", user_file_path, test_code_js)

    if success:
        print("JavaScript tests succeeded! Output:")
        print(output)
    else:
        print("JavaScript tests failed! Error:")
        print(output)
