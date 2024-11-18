import subprocess

def run_test(user_code, test_code):
    try:
        #Fussionne les deux fichiers
        full_code = f"{user_code}\n{test_code}"

        #Le mettre dans un fichier temporaire
        with open("temp_script.py", "w") as temp_file:
            temp_file.write(full_code)
        #Lance le script
        result = subprocess.run(
            ["python", "temp_script.py"],
            capture_output=True,
            text=True,
            timeout=5
        )

        # Vérifier si le test a réussi
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr

    except subprocess.TimeoutExpired:
        return False, "Execution timed out."
    except Exception as e:
        return False, str(e)
