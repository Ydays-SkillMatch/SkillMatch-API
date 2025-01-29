import subprocess
import os
from datetime import datetime
from app.Models.Exercice import Exercice
from app.Views.Controller import Controller
from app.Correct import Correct


class SubmitCode(Controller):
    

    def post(self, request):
        exercise_id = request.GET.get("uuid")
        exercise = Exercice.objects.get(uuid=exercise_id)
        test = f"app/exercice/{exercise.ex_language.name.lower()}/exe/{datetime.now()}.{exercise.ex_language.extension}"
        os.makedirs(f"app/exercice/{exercise.ex_language.name.lower()}/exe/",exist_ok=True)
        with open(test, "w") as file:
            file.write(request.POST.get('Test'))
        print(Correct(exercise.test, test, exercise.correct, exercise.name))
    
    def run_code_in_docker(language, user_file_path, test_code):
        try:
            file_extension = {"python": "py", "javascript": "js", "php": "php"}
            docker_images = {"python": "python:3.12-slim", "javascript": "node:latest", "php": "php:latest"}

            if language not in file_extension or language not in docker_images:
                return False, f"Unsupported language: {language}"

            ext = file_extension[language]
            temp_test_filename = f"temp_test_script.{ext}"

            # Lire le fichier utilisateur
            with open(user_file_path, "r") as user_file:
                user_code = user_file.read()

            # Combiner le code utilisateur et le code de test
            full_code = f"{user_code}\n{test_code}"

            # Écrire le code combiné dans un fichier temporaire
            with open(temp_test_filename, "w") as temp_file:
                temp_file.write(full_code)

            # Commande Docker pour exécuter le fichier
            result = subprocess.run(
                [
                    "docker", "run", "--rm", "-v",
                    f"{os.getcwd()}:/app",
                    docker_images[language],
                    language if language == "php" else "node" if language == "javascript" else "python",
                    temp_test_filename
                ],
                capture_output=True,
                text=True,
                timeout=10
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
            # Supprimer le fichier temporaire de test
            if os.path.exists(temp_test_filename):
                os.remove(temp_test_filename)
                
            
            