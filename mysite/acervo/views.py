from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    def get(self, request, *args, **kwargs):
        # Renderiza o template de login quando a requisição é GET
        return render(request, 'acervo/login.html')
    
    def post(self, request, *args, **kwargs):
        # Obtém os dados do formulário POST
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Tenta autenticar o usuário
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Se a autenticação for bem-sucedida, realiza o login do usuário
            login(request, user)
            # Redireciona para a página inicial ou para a página de sucesso
            return redirect(reverse('cadastrar-item'))  # Ajuste 'home' para a URL desejada após o login
        else:
            # Se a autenticação falhar, renderiza o template com uma mensagem de erro
            return render(request, 'acervo/login.html', {'error': 'Nome de usuário ou senha incorretos.'})

class CadastroView(View):
    def get(self, request, *args, **kwargs):
        # Renderiza o template de cadastro quando a requisição é GET
        return render(request, 'acervo/cadastro.html')
    
    def post(self, request, *args, **kwargs):
        # Obtém os dados do formulário POST
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verifica se todos os campos estão preenchidos
        if email and username and password:
            # Verifica se o nome de usuário ou email já existem
            if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
                # Cria um novo usuário e o salva
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                # Redireciona para a página de login
                return redirect(reverse('login'))
            else:
                # Se o nome de usuário ou email já existirem, renderiza o template com uma mensagem de erro
                return render(request, 'acervo/cadastro.html', {'error': 'Nome de usuário ou email já existe.'})
        else:
            # Se algum campo estiver faltando, renderiza o template com uma mensagem de erro
            return render(request, 'acervo/cadastro.html', {'error': 'Por favor, preencha todos os campos obrigatórios.'})

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        # Desloga o usuário atual
        logout(request)
        # Redireciona para a página de login ou qualquer outra página desejada
        return redirect(reverse('login'))

class CadastrarItemView(LoginRequiredMixin, View):
    # Redefine o método get para renderizar o template
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/cadastrar-item.html')

    # Adiciona uma classe de erro se o usuário não estiver autenticado
    def handle_no_permission(self):
        # Redireciona para a página de login, ou qualquer outra página de sua escolha
        return redirect('login')