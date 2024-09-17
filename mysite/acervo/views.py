from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import Item, Contato, Emprestimo
from django.contrib import messages
from datetime import date

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
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/cadastrar-item.html')
    def handle_no_permission(self):
        return redirect('login')
    
    def post(self, request, *args, **kwargs):
        titulo = request.POST.get('titulo')
        autor = request.POST.get('autor')
        ano = request.POST.get('ano')
        imagem = request.FILES.get('imagem')

        # Validação e criação do item
        if titulo and autor and ano:
            item = Item.objects.create(
                titulo=titulo,
                autor=autor,
                ano=ano,
                imagem=imagem
            )
            return redirect(reverse('itens-disponiveis'))
        else:
            messages.error(request, 'Por favor, preencha todos os campos obrigatórios.')
            return render(request, 'acervo/cadastrar-item.html')
    
class AdicionarContatoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'acervo/adicionar-contato.html')

    def post(self, request, *args, **kwargs):
        nome = request.POST.get('nome')
        email = request.POST.get('email')

        # Validação e criação do Contato
        if nome and email:
            contato = Contato.objects.create(
                nome = nome,
                email = email
            )
            return redirect(reverse('registrar-emprestimo'))

        return render(request, 'acervo/adicionar-contato.html')

    def handle_no_permission(self):
        return redirect('login')
    
class EmprestimoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        itens = Item.objects.filter(status='disponivel')
        contatos = Contato.objects.all()

        contexto = {'itens': itens, 'contatos': contatos}

        return render(request, 'acervo/registrar-emprestimo.html', contexto)

    def post(self, request, *args, **kwargs):
        item_id = request.POST.get('item')
        contato_id = request.POST.get('contato')
        data_emprestimo = request.POST.get('data-emprestimo')

        if item_id and contato_id:
            item = Item.objects.get(id=item_id)
            contato = Contato.objects.get(id=contato_id)

            Emprestimo.objects.create(
                item = item,
                contato = contato, 
                data_emprestimo = data_emprestimo,
            )

            item.status = 'emprestado'
            item.save()

            return redirect(reverse('itens-emprestados'))

        return render(request, 'acervo/registrar-emprestimo.html')

    def handle_no_permission(self):
        return redirect('login')
    
class DevolucaoView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Filtra apenas os empréstimos que não foram devolvidos
        emprestimos_nao_devolvidos = Emprestimo.objects.filter(devolvido=False)

        contexto = {"emprestimos": emprestimos_nao_devolvidos}

        return render(request, 'acervo/registrar-devolucao.html', contexto)
    
    def post(self, request, *args, **kwargs):
        emprestimo_id = request.POST.get('emprestimo')

        if emprestimo_id:
            emprestimo = Emprestimo.objects.get(id=emprestimo_id)

            # Atualiza a data de devolução e o status
            emprestimo.data_devolucao = date.today()
            emprestimo.devolvido = True

            # Atualiza o status do item para "disponível"
            emprestimo.item.status = 'disponivel'
            emprestimo.item.save()

            emprestimo.save()  # Salva o objeto Emprestimo com as alterações

            # Redireciona para a página de itens disponíveis após a devolução
            return redirect(reverse('itens-disponiveis'))

        # Em caso de erro, repete o método GET
        emprestimos_nao_devolvidos = Emprestimo.objects.filter(devolvido=False)
        contexto = {"emprestimos": emprestimos_nao_devolvidos}
        return render(request, 'acervo/registrar-devolucao.html', contexto)

    def handle_no_permission(self):
        return redirect('login')

class ItensDisponiveisView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        itens = Item.objects.filter(status='disponivel')
        
        # Passar os itens para o template
        contexto = {'itens': itens}

        return render(request, 'acervo/itens-disponiveis.html', contexto)
    
    def handle_no_permission(self):
        return redirect('login')

class ItensEmprestadosView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        itens = Item.objects.filter(status='emprestado')
        
        # Passar os itens para o template
        contexto = {'itens': itens}

        return render(request, 'acervo/itens-emprestados.html', contexto)
    
    def handle_no_permission(self):
        return redirect('login')
    
