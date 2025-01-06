from django.shortcuts import get_object_or_404

from app.functionTest.testRunner import run_test
from app.Models import Exercise, submitCode
from app.Views.Controller import Controller


class ExerciceSubmit(Controller):

    def post(self, request, exercise_id):

        exercise = get_object_or_404(Exercise, id=exercise_id)
        user_code = request.data.get("user_code")

        if not user_code:
            return self.response({"error": "Code utilisateur non fourni."}, status=400)

        is_correct, output = run_test(user_code, exercise.test_code)

        submission = submitCode.objects.create(
            user=request.user,
            exercise=exercise,
            user_code=user_code,
            is_correct=is_correct
        )

        # Retourner le résultat en JSON
        return self.response({
            "is_correct": is_correct,
            "output": output
        })
