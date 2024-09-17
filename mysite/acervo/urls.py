from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('cadastro/', views.CadastroView.as_view(), name="cadastro"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('cadastrar-item/', views.CadastrarItemView.as_view(), name="cadastrar-item"),
    path('adicionar-contato/', views.AdicionarContatoView.as_view(), name="adicionar-contato"),
    path('registrar-emprestimo/', views.EmprestimoView.as_view(), name="registrar-emprestimo"),
    path('registrar-devolucao/', views.DevolucaoView.as_view(), name="registrar-devolucao"),
    path('itens-disponiveis/', views.ItensDisponiveisView.as_view(), name="itens-disponiveis"),
    path('itens-emprestados/', views.ItensEmprestadosView.as_view(), name="itens-emprestados"),
] 