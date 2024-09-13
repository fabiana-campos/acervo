from django.urls import path
from . import views
from . import auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('itens/', views.listar_itens, name='listar_itens'),
    path('cadastrar-item/', views.cadastrar_item, name='cadastrar_item'),
    path('contatos/', views.listar_contatos, name='listar_contatos'),
    path('cadastrar-contato/', views.cadastrar_contato, name='cadastrar_contato'),
    path('emprestimos/', views.gerenciar_emprestimos, name='gerenciar_emprestimos'),
    path('registrar-emprestimo/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('marcar-devolvido/<int:emprestimo_id>/', views.marcar_devolvido, name='marcar_devolvido'),
]
