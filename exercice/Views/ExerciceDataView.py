import os
import uuid

from django.db.migrations import serializer
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib import messages
from language.models import Language
from skillmatch.MasterViews.BaseView import BaseView
from exercice.models import Exercice
from exercice.serializers import ExerciceDataSerializer

class ExerciceDataView(BaseView):
    serializer_class = ExerciceDataSerializer
    model_class = Exercice

    def __init__(self):
        super().__init__()

    def get(self, request):
        getuuid = request.GET.get('uuid')
        if getuuid != None:
            test_exercice = Exercice.objects.get(uuid=getuuid)
            if not test_exercice:
                return Response({"error": "Exercice not found"}, status=404)
        else:
            test_exercice = Exercice.objects.all()
        return super().serialize(test_exercice,"user")

    def post(self, request):
        os.makedirs("app/exercice/python/test/", exist_ok=True)
        os.makedirs("app/exercice/python/correct/", exist_ok=True)
        name = request.POST.get('name')
        describe = request.POST.get('describe')
        timer = request.POST.get('timer')
        language = Language.objects.get(uuid=request.POST.get('language'))
        uuid2 = uuid.uuid4()
        test = f"app/exercice/python/test/{uuid2}.txt"
        correct = f"app/exercice/python/correct/{uuid2}.py"
        new_test = Exercice(uuid=uuid2, name=name, describe=describe, timer=timer, ex_language=language, test=test,
                            correct=correct)
        new_test.save()
        with open(test, "w") as file:
            file.write(request.POST.get('Test'))
        messages.success(request, "Formulaire soumis avec succès !")
        return JsonResponse(serializer.data, safe=False)