from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import  RegisterSerializer

# Create your views here.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer