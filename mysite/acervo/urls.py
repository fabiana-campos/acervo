from django.urls import path
from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('cadastro/', views.CadastroView.as_view(), name="cadastro"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('cadastrar-item/', views.CadastrarItemView.as_view(), name="cadastrar-item"),
]