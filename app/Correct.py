import json
def Correct(file, user_code, correct_code, name) :
    user_code = user_code.split(".")[0].replace("/", ".")
    exec(f"import {user_code}")
    with open(f"{file}", "r", encoding="utf-8") as file:
        for ligne in file:
            args = ligne.split(",")
            if user_code.add(args[0]) != correct_code.add(args[1]):
                return json.dumps({"Validate": "False", "Input": ligne, "Obtain": user_code(ligne), "Expected": correct_code(ligne)})
            
    return json.dumps({"Validate": "True"})
            