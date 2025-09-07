# from django.http import JsonResponse
from drf_spectacular.openapi import AutoSchema
from django.contrib import messages
from app.Models.Language import Language
from app.Views.Controller import Controller
from drf_yasg.utils import swagger_auto_schema
from app.serializers.Serializer import LanguageSerializer


class LanguageController(Controller):
    schema = AutoSchema()
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get language with the ORM here
        getid = request.GET.get('id')
        # this line create a new language, its just to show you the serializer
        if getid != None :
            test_language = Language.objects.get(id=getid)
        else :
            test_language = Language.objects.all()
        return super().serialize(test_language, "user") #this route is a "user" type route, this mean only uuid will be returned, 
        # if you want to also return created_at, use "admin"
    
    
    @swagger_auto_schema(
        request_body=LanguageSerializer,  # Serializer utilisé pour documenter le corps de la requête
        responses={201: "New Language Added", 400: "Invalid input"}
    )
    # @api_view(['POST'])        
    def post(self,request):
        name = request.POST.get('Name') if request.POST.get('Name') != None else request.data.get('name')
        ext = request.POST.get('Extension') if request.POST.get('Extension') != None else request.data.get('extension')
        new_language = Language(name=name.upper(),extension=ext.lower())
        new_language.save()
        messages.success(request, "Formulaire soumis avec succès !")
        return super().serialize(new_language, "user")
        