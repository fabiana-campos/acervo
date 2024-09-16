from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User

class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/login.html')

class CadastroView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/cadastro.html')
    
    def post(self, request, *args, **kwargs):
        print('entrou no post')