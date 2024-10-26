from django.http import JsonResponse

from app.Models.User import User
from app.Views.Controller import Controller


class UserController(Controller):
    
    def __init__(self):
        super().__init__()
    
    def get(self, request):
        # you are suppose to get users with the ORM here
        
        # this line create a new user, its just to show you the serializer
        test_user = User(username="test",email="test@test")
        return super().serialize(test_user, "user") #this route is a "user" type route, this mean only uuid will be returned, if you want to also return created_at, use "admin"