import subprocess
import os

def run_test(user_code, test_code, language="python"):
    try:
        # Dictionnaires pour gérer les extensions et les commandes par langage
        file_extension = {"python": "py", "javascript": "js", "java": "java"}
        interpreters = {
            "python": ["python"],
            "javascript": ["node"],
            "java": ["javac", "java"]
        }

        # Vérifier si le langage est pris en charge
        if language not in file_extension or language not in interpreters:
            return False, f"Unsupported language: {language}"

        ext = file_extension[language]
        temp_filename = f"temp_script.{ext}"
        full_code = f"{user_code}\n{test_code}"

        # Écrire le code dans un fichier temporaire
        with open(temp_filename, "w") as temp_file:
            temp_file.write(full_code)

        if language == "java":
            # Compilation et exécution pour Java
            compile_result = subprocess.run(
                ["javac", temp_filename],
                capture_output=True,
                text=True,
                timeout=5
            )
            if compile_result.returncode != 0:
                return False, compile_result.stderr

            # Lancer le fichier compilé
            class_name = temp_filename.replace(".java", "")
            result = subprocess.run(
                ["java", class_name],
                capture_output=True,
                text=True,
                timeout=5
            )
            #Interprete le JS et python
        else:
            result = subprocess.run(
                interpreters[language] + [temp_filename],
                capture_output=True,
                text=True,
                timeout=5
            )

        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Execution timed out."
    except Exception as e:
        return False, str(e)
    finally:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        if language == "java" and os.path.exists("temp_script.class"):
            os.remove("temp_script.class")
