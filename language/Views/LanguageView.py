from django.contrib import messages
from skillmatch.MasterViews.BaseView import BaseView
from language.models import Language
from language.serializers import LanguageSerializer

class LanguageView(BaseView):
    serializer_class = LanguageSerializer
    model_class = Language

    def __init__(self):
        super().__init__()

    def get(self, request):
        getid = request.GET.get('id')
        if getid != None:
            test_language = Language.objects.get(id=getid)
        else:
            test_language = Language.objects.all()
        return super().serialize(test_language,
                                 "user")

    def post(self, request):
        name = request.POST.get('Name')
        new_language = Language(name=name.upper())
        new_language.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_language, "user")
