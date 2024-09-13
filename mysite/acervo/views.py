from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from .models import Item, Contato, Emprestimo
from .forms import ItemForm, ContatoForm, EmprestimoForm

class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('home')
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    template_name = 'login.html'

class LogoutView(View):
    def get(self, request):
        return redirect('login')

class CadastrarItemView(View):
    def get(self, request):
        form = ItemForm()
        return render(request, 'cadastrar-item.html', {'form': form})

    def post(self, request):
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item cadastrado com sucesso!')
            return redirect('home')
        return render(request, 'cadastrar-item.html', {'form': form})

class RegistrarEmprestimoView(View):
    def get(self, request):
        form = EmprestimoForm()
        return render(request, 'registrar-emprestimo.html', {'form': form})

    def post(self, request):
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empréstimo registrado com sucesso!')
            return redirect('home')
        return render(request, 'registrar-emprestimo.html', {'form': form})

class RegistrarDevolucaoView(View):
    def get(self, request):
        form = EmprestimoForm()
        return render(request, 'registrar-devolucao.html', {'form': form})

    def post(self, request):
        form = EmprestimoForm(request.POST)
        if form.is_valid():
            emprestimo = form.save(commit=False)
            emprestimo.devolvido = True
            emprestimo.save()
            messages.success(request, 'Devolução registrada com sucesso!')
            return redirect('home')
        return render(request, 'registrar-devolucao.html', {'form': form})

class ListarItensView(View):
    def get(self, request):
        itens_disponiveis = Item.objects.filter(status='disponivel')
        itens_emprestados = Item.objects.filter(status='emprestado')
        return render(request, 'listar-itens.html', {'itens_disponiveis': itens_disponiveis, 'itens_emprestados': itens_emprestados})

class AdicionarContatoView(View):
    def get(self, request):
        form = ContatoForm()
        return render(request, 'adicionar-contato.html', {'form': form})

    def post(self, request):
        form = ContatoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contato adicionado com sucesso!')
            return redirect('home')
        return render(request, 'adicionar-contato.html', {'form': form})


